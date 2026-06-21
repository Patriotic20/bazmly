from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator

T = TypeVar("T")

LowerStr = Annotated[str, BeforeValidator(lambda v: v.strip().lower() if isinstance(v, str) else v)]


class BaseSchema(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def strip_strings(cls, values):
        if isinstance(values, dict):
            return {k: v.strip() if isinstance(v, str) else v for k, v in values.items()}
        return values


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)

    @property
    def limit(self) -> int:
        return self.size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
