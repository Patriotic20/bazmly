from app.core.database.base import Base
from app.core.database.id_uuid_pk import IdUuidPk
from app.core.database.time_stamp_mixin import TimeStampMixin


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.review.model import Review
    from app.modules.menu_item.model import MenuItem
    from app.modules.venue_image.model import VenueImage
    from app.modules.order.model import Order
    from app.modules.reservation.model import Reservation

class Restaurant(IdUuidPk, TimeStampMixin, Base):
    __tablename__ = "restaurants"

    name: Mapped[str] = mapped_column(String, index=True)

    address: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    reviews: Mapped[list["Review"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")
    menu_items: Mapped[list["MenuItem"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")
    images: Mapped[list["VenueImage"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")
