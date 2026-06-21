import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.id_uuid_pk import IdUuidPk
from app.core.database.time_stamp_mixin import TimeStampMixin
from app.modules.reservation.enums import ReservationStatus

if TYPE_CHECKING:
    from app.modules.restaurant.model import Restaurant
    from app.modules.user.model import User


class Reservation(IdUuidPk, TimeStampMixin, Base):
    __tablename__ = "reservations"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    restaurant_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("restaurants.id", ondelete="CASCADE"))
    guest_count: Mapped[int] = mapped_column(Integer)
    reservation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[ReservationStatus] = mapped_column(SAEnum(ReservationStatus), default=ReservationStatus.PENDING)

    user: Mapped["User"] = relationship(back_populates="reservations")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="reservations")
