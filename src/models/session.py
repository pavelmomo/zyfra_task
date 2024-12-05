from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from db.utils import TZDateTime


class Session(Base):
    """
    Модель таблицы сессий
    """

    __tablename__ = "session"
    id: Mapped[str] = mapped_column(primary_key=True)
    expiration_date: Mapped[datetime] = mapped_column(TZDateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="sessions", lazy="raise")
