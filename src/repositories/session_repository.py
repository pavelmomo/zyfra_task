from sqlalchemy import delete

from db.db_sqlite import database
from models.session import Session


class SessionRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def get_by_id(self, session_id: str) -> Session | None:
        async with self.db.session_factory() as session:
            result = await session.get(Session, session_id)
            return result

    async def create(self, session_obj: Session) -> None:
        async with self.db.session_factory() as session:
            session.add(session_obj)
            await session.commit()

    async def delete(self, session_id: str) -> None:
        async with self.db.session_factory() as session:
            statement = delete(Session).where(Session.id == session_id)
            await session.execute(statement)
            await session.commit()


session_repository = SessionRepository(database)
