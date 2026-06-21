import uuid
from app.core.database.base import Base
from app.core.database.id_uuid_pk import IdUuidPk
from app.core.database.time_stamp_mixin import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Uuid, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.restaurant.model import Restaurant

class VenueImage(IdUuidPk, TimeStampMixin, Base):
    __tablename__ = "venue_images"

    image_url: Mapped[str] = mapped_column(String, nullable=False)
    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_main: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    restaurant: Mapped["Restaurant"] = relationship(back_populates="images")