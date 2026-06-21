from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.id_uuid_pk import IdUuidPk
from app.core.database.time_stamp_mixin import TimeStampMixin

if TYPE_CHECKING:
    from app.modules.order.model import Order
    from app.modules.reservation.model import Reservation
    from app.modules.review.model import Review


class User(IdUuidPk, TimeStampMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True, index=True)
    password: Mapped[str | None] = mapped_column(String, nullable=True)
    google_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True, index=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    orders: Mapped[list["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")
