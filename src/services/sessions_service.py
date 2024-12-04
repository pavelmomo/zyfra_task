import hashlib
import uuid
from datetime import datetime, timedelta, timezone

from common.exceptions import (CredentialExpiredException,
                               InvalidCredentialException, NotFoundException)
from common.settings import settings
from models.session import Session
from repositories.session_repository import session_repository
from repositories.user_repository import user_repository


class SessionService:

    async def check_session(self, session_id: str) -> None:             # проверка сессии
        found_session = await session_repository.get_by_id(session_id)
        if found_session is None:
            raise NotFoundException()
        if not self._validate_session_expiration(found_session.expiration_date):
            await self.delete_session(found_session.id)
            raise CredentialExpiredException()

    async def delete_session(self, session_id: str) -> None:            # удаление сессии
        found_session = await session_repository.get_by_id(session_id)
        if found_session is None:
            raise NotFoundException()
        await session_repository.delete(session_id)

    async def authenticate(self, login: str, password: str) -> int:     # аутентификация
        found_user = await user_repository.get_by_login(login)
        if found_user is None:  # проверка на наличие логина
            raise NotFoundException()
        stored_pass = found_user.password
        if (
            not stored_pass == hashlib.sha256(password.encode()).hexdigest()
        ):  # проверка хэша пароля
            raise InvalidCredentialException()
        return found_user.id

    async def generate_and_save_session(
        self, user_id
    ) -> str:                                                   # генерация и сохранение данных сессии
        new_session_id = str(uuid.uuid4())                      
        exp_time = datetime.now(timezone.utc) + timedelta(
            minutes=settings.SESSION_TTL
        )                                                       # вычисление даты истечения сессии

        new_session = Session(
            id=new_session_id, expiration_date=exp_time, user_id=user_id
        )
        await session_repository.create(new_session)
        return new_session_id

    def _validate_session_expiration(
        self, session_expire_date: datetime
    ) -> bool:                                                  # проверка истечения срока сессии
        if session_expire_date > datetime.now(timezone.utc):
            return True
        return False


session_service = SessionService()
