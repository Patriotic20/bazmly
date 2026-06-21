import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.core.schemas.base import BaseSchema


class OrderItemCreate(BaseSchema):
    order_id: uuid.UUID
    menu_item_id: uuid.UUID
    quantity: int = 1
    price_at_order: Decimal


class OrderItemUpdate(BaseSchema):
    quantity: int | None = None


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    menu_item_id: uuid.UUID
    quantity: int
    price_at_order: Decimal
