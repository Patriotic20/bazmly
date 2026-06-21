import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.core.schemas.base import BaseSchema
from app.modules.order.enums import OrderStatus


class OrderCreate(BaseSchema):
    user_id: uuid.UUID
    restaurant_id: uuid.UUID
    reservation_id: uuid.UUID | None = None


class OrderUpdate(BaseSchema):
    status: OrderStatus | None = None
    total_price: Decimal | None = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    restaurant_id: uuid.UUID
    reservation_id: uuid.UUID | None
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
