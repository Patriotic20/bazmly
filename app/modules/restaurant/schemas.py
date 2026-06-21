import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.schemas.base import BaseSchema, LowerStr


class RestaurantCreate(BaseSchema):
    name: LowerStr
    address: LowerStr | None = None
    description: str | None = None


class RestaurantUpdate(BaseSchema):
    name: LowerStr | None = None
    address: LowerStr | None = None
    description: str | None = None


class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    address: str | None
    description: str | None
    created_at: datetime
