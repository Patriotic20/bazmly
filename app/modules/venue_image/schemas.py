import uuid

from pydantic import BaseModel, ConfigDict

from app.core.schemas.base import BaseSchema


class VenueImageCreate(BaseSchema):
    image_url: str
    restaurant_id: uuid.UUID
    is_main: bool = False


class VenueImageUpdate(BaseSchema):
    image_url: str | None = None
    is_main: bool | None = None


class VenueImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    image_url: str
    restaurant_id: uuid.UUID
    is_main: bool
