import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.core.schemas.base import BaseSchema, LowerStr


class MenuItemCreate(BaseSchema):
    name: LowerStr
    price: Decimal
    image_url: str
    restaurant_id: uuid.UUID


class MenuItemUpdate(BaseSchema):
    name: LowerStr | None = None
    price: Decimal | None = None
    image_url: str | None = None


class MenuItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    price: Decimal
    image_url: str
    restaurant_id: uuid.UUID
