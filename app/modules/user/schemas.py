import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.schemas.base import BaseSchema, LowerStr


class UserCreate(BaseSchema):
    username: LowerStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    created_at: datetime
