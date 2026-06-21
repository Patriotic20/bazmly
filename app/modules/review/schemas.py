import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.schemas.base import BaseSchema


class ReviewCreate(BaseSchema):
    stars: int = Field(ge=1, le=5)
    text: str
    user_id: uuid.UUID
    restaurant_id: uuid.UUID


class ReviewUpdate(BaseSchema):
    stars: int | None = Field(None, ge=1, le=5)
    text: str | None = None


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    stars: int
    text: str
    user_id: uuid.UUID
    restaurant_id: uuid.UUID
    created_at: datetime
