import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Uuid
from app.core.database.base import Base
from app.core.database.id_uuid_pk import IdUuidPk
from app.core.database.time_stamp_mixin import TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.order.model import Order
    from app.modules.reservation.model import Reservation
    from app.modules.review.model import Review

class User(IdUuidPk, TimeStampMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)

    orders: Mapped[list["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")
