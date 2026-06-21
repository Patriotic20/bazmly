import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.id_uuid_pk import IdUuidPk
from app.core.database.time_stamp_mixin import TimeStampMixin

if TYPE_CHECKING:
    from app.modules.order_item.model import OrderItem
    from app.modules.restaurant.model import Restaurant


class MenuItem(IdUuidPk, TimeStampMixin, Base):
    __tablename__ = "menu_items"

    name: Mapped[str] = mapped_column(String)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    image_url: Mapped[str] = mapped_column(String)
    restaurant_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("restaurants.id", ondelete="CASCADE"))

    restaurant: Mapped["Restaurant"] = relationship(back_populates="menu_items")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="menu_item", cascade="all, delete-orphan")
