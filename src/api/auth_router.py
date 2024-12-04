from fastapi import APIRouter, Body, HTTPException, Response, status

from common.exceptions import (
    CredentialExpiredException,
    InvalidCredentialException,
    NotFoundException,
)
from services.sessions_service import session_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", summary="Создание новой сессии")
async def authenticate(login=Body(embed=True), password=Body(embed=True)):
    try:
        user_id = await session_service.authenticate(login, password)
        new_session_id = await session_service.generate_and_save_session(user_id)
        return Response(
            f"Вы успешно авторизовались. Новый id сессии: {new_session_id}",
            media_type="text",
        )

    except (NotFoundException, InvalidCredentialException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e


@auth_router.post("/session", summary="Проверка сессии на существование")
async def check_session(session_id=Body(embed=True)):
    try:
        await session_service.check_session(session_id)
        return Response("Вы успешно вошли в систему", media_type="text")

    except (NotFoundException, CredentialExpiredException) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        ) from e


@auth_router.delete("/session", summary="Удаление сессии")
async def delete_session(session_id=Body(embed=True)):
    try:
        await session_service.delete_session(session_id)
        return Response("Сессия успешно удалена", media_type="text")

    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
