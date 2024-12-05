from sqlalchemy import select

from db.db_sqlite import database
from models.user import User


class UserRepository:

    def __init__(self, db) -> None:
        self.db = db

    async def get_by_login(self, login: str) -> User | None:
        async with self.db.session_factory() as session:
            statement = select(User).where(User.login == login)
            exec_result = await session.execute(statement)
            result = exec_result.scalar_one_or_none()
            return result


user_repository = UserRepository(database)
