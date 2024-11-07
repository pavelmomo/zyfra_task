import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone

SESSION_TTL = 5
USER_FILENAME = "user-credits.json"
SESSION_FILENAME = "active-sessions.json"

# данные о пользователях хранятся под ключом users, в формате логин:пароль
# данные о сессиях хранятся под ключом sessions, в формате id сессии:дата истечения
app_data: dict[str, dict[str, str]] = {}


def init_storage():
    if not os.path.exists(USER_FILENAME):
        print("Ошибка: Не был найден файл с учетными данными пользователей")
        sys.exit(1)
    else:
        with open(USER_FILENAME, "r", encoding="utf-8") as file:
            app_data["users"] = json.load(file)

    if not os.path.exists(SESSION_FILENAME):
        write_sessions({})
        app_data["sessions"] = {}
    else:
        with open(SESSION_FILENAME, "r", encoding="utf-8") as file:
            app_data["sessions"] = json.load(file)


def write_sessions(sessions: dict):
    with open(SESSION_FILENAME, "w", encoding="utf-8") as file:
        json.dump(sessions, file)


def validate_session_expiration(session_id: str) -> bool:
    if datetime.fromisoformat(app_data["sessions"][session_id]) > datetime.now(
        timezone.utc
    ):
        return True
    return False


def check_session_id(session_id: str) -> bool:
    if session_id in app_data["sessions"]:
        if validate_session_expiration(session_id):
            print("Вы вошли в систему")
            return True
        print("Время жизни сессии истекло")
    else:
        print("Введённая сессия не найдена")
    return False


def delete_session(session_id: str):
    if session_id in app_data["sessions"]:
        del app_data["sessions"][session_id]
        write_sessions(app_data["sessions"])
        print(f"Сессия {session_id} удалена")
    else:
        print("Введённая для удаления сессия не найдена")


def authenticate(login: str, password: str) -> bool:
    if login not in app_data["users"]:
        print("Указанный пользовтель не найден")
        return False
    stored_pass = app_data["users"][login]
    if stored_pass == hashlib.sha256(password.encode()).hexdigest():
        print("Пользователь успешно прошел аутентификацию")
        return True
    print("Введён неверный пароль")
    return False


def generate_and_save_session() -> str:
    new_session_id = str(uuid.uuid4())
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=SESSION_TTL)
    app_data["sessions"][new_session_id] = exp_time.isoformat()
    write_sessions(app_data["sessions"])
    return new_session_id


def teletype():
    while True:
        typed_session_id = input("Введите идентификатор сессии: ")

        splited_input = typed_session_id.split()
        if len(splited_input) == 2 and "delete" in splited_input:
            delete_session(splited_input[1])
            continue
        if check_session_id(typed_session_id):
            break  # выход после успешного ввода сессии

        while True:
            login = input("Введите логин : ")
            password = input("Введите пароль : ")
            if authenticate(login, password):
                # генерация идентификатора сессии и сохранение в файл
                new_session_id = generate_and_save_session()
                print(f"Новый идентификатор сессии: {new_session_id}")
                break


if __name__ == "__main__":
    if len(sys.argv) == 2:
        USER_FILENAME = sys.argv[1]
    init_storage()
    teletype()
