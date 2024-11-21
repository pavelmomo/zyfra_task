import hashlib
import json
import os
import uuid
from datetime import datetime, timedelta, timezone

from common.exceptions import (AppException, CredentialExpiredException,
                               InvalidCredentialException, NotFoundException)
from common.settings import settings


class SessionService:
    # данные о пользователях хранятся под ключом users, в формате логин:пароль
    # данные о сессиях хранятся под ключом sessions, в формате id сессии:дата истечения
    users_data: dict[str, str] = {}
    sessions_data: dict[str, str] = {}
    def init_storage(self) -> None:                                             # проверка и считываение данных из файлов
        if not os.path.exists(settings.USER_FILENAME):                          # проверка на существование файла с пользователями
            raise AppException("Не был найден файл с учётными данными пользователей")

        with open(settings.USER_FILENAME, "r", encoding="utf-8") as file:       # считывание данных из файла
            self.users_data = json.load(file)

        if not os.path.exists(settings.SESSION_FILENAME):                       # проверка на существование файла с сессиями
            self._write_sessions({})                                            # создание пустого файла с сессиями
            self.sessions_data = {}
        else:                                                                   # считывание данных из файла
            with open(settings.SESSION_FILENAME, "r", encoding="utf-8") as file: 
               self.sessions_data = json.load(file)


    def _write_sessions(self, sessions: dict) -> None:                          # запись сессий в файл
        with open(settings.SESSION_FILENAME, "w", encoding="utf-8") as file:
            json.dump(sessions, file)


    def _validate_session_expiration(self, session_id: str) -> bool:            # проверка истечения срока сессии
        if datetime.fromisoformat(self.sessions_data[session_id]) > datetime.now(
            timezone.utc
        ):
            return True
        return False


    def check_session_id(self, session_id: str) -> None:                        # проверка сессии
        if session_id not in self.sessions_data:
            raise NotFoundException()
        if not self._validate_session_expiration(session_id):
            raise CredentialExpiredException()


    def delete_session(self, session_id: str) -> None:                           # удаление сессии
        if not session_id in self.sessions_data:
            raise NotFoundException()
        del self.sessions_data[session_id]
        self._write_sessions(self.sessions_data)


    def authenticate(self, login: str, password: str):                          # аутентификация
        if login not in self.users_data:                                        # проверка на наличие логина
            raise NotFoundException()
        stored_pass = self.users_data[login]
        if not stored_pass == hashlib.sha256(password.encode()).hexdigest():    # проверка хэша пароля
            raise InvalidCredentialException()


    def generate_and_save_session(self) -> str:                                # генерация и сохранение данных сессии
        new_session_id = str(uuid.uuid4())                                     # генерация id сессии
        exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.SESSION_TTL)  # вычисление даты истечения сессии
        self.sessions_data[new_session_id] = exp_time.isoformat()
        self._write_sessions(self.sessions_data)                                # запись изменений в файл
        return new_session_id

session_service = SessionService()
