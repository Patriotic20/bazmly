import uuid
from datetime import datetime

from pydantic import AwareDatetime, BaseModel, ConfigDict

from app.core.schemas.base import BaseSchema
from app.modules.reservation.enums import ReservationStatus


class ReservationCreate(BaseSchema):
    user_id: uuid.UUID
    restaurant_id: uuid.UUID
    guest_count: int
    reservation_time: AwareDatetime


class ReservationUpdate(BaseSchema):
    status: ReservationStatus | None = None
    guest_count: int | None = None
    reservation_time: AwareDatetime | None = None


class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    restaurant_id: uuid.UUID
    guest_count: int
    reservation_time: datetime
    status: ReservationStatus
    created_at: datetime
