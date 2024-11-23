from fastapi import APIRouter, Body, HTTPException, Response, status

from common.exceptions import (CredentialExpiredException,
                               InvalidCredentialException, NotFoundException)
from services.sessions_service import session_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", summary="Создание новой сессии")
async def authenticate(login=Body(embed=True), password=Body(embed=True)):
    try:
        session_service.authenticate(login, password)
        new_session_id = session_service.generate_and_save_session()
        return Response(
            f"Вы успешно авторизовались. Новый id сессии: {new_session_id}",
            media_type="text",
        )

    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не существует",
        ) from e
    except InvalidCredentialException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Был введён неправильный пароль",
        ) from e


@auth_router.post("/session", summary="Проверка сессии на существование")
async def check_session(session_id=Body(embed=True)):
    try:
        session_service.check_session_id(session_id)
        return Response("Вы успешно вошли в систему", media_type="text")

    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия не существует",
        ) from e
    except CredentialExpiredException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия сессии истёк",
        ) from e


@auth_router.delete("/session", summary="Удаление сессии")
async def delete_session(session_id=Body(embed=True)):
    try:
        session_service.delete_session(session_id)
        return Response("Сессия успешно удалена", media_type="text")

    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия не существует",
        ) from e
