from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class User(Base):
    """
    Модель таблицы пользователей
    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    sessions: Mapped[List["Session"]] = relationship(
        back_populates="user", lazy="raise"
    )
