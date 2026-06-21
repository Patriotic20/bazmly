import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum as SAEnum, ForeignKey, Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.id_uuid_pk import IdUuidPk
from app.core.database.time_stamp_mixin import TimeStampMixin
from app.modules.order.enums import OrderStatus

if TYPE_CHECKING:
    from app.modules.order_item.model import OrderItem
    from app.modules.reservation.model import Reservation
    from app.modules.restaurant.model import Restaurant
    from app.modules.user.model import User


class Order(IdUuidPk, TimeStampMixin, Base):
    __tablename__ = "orders"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))
    restaurant_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("restaurants.id", ondelete="CASCADE"))
    reservation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid, ForeignKey("reservations.id", ondelete="SET NULL"), nullable=True
    )
    total_price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), default=Decimal("0.00"))
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDING)

    user: Mapped["User"] = relationship(back_populates="orders")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    reservation: Mapped[Optional["Reservation"]] = relationship()
