from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from common.exceptions import DbConnectionException


class DatabaseSqlite:
    engine: AsyncEngine
    session_factory: async_sessionmaker
    url: str = "sqlite+aiosqlite:///sessions.db"
        
    async def init_db(self):
        try:
            self.engine = create_async_engine(url=self.url, echo=False)
            await self._create_and_init_tables(self.engine)
            self.session_factory = async_sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )

        except (OSError, SQLAlchemyError) as e:
            raise DbConnectionException from e

    async def _create_and_init_tables(self, engine: AsyncEngine):
        from models.base import Base
        from models.session import Session
        from models.user import User
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)

database = DatabaseSqlite()
