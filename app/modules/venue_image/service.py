import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repository.base import BaseRepository
from app.core.schemas.base import PaginatedResponse
from app.modules.venue_image.model import VenueImage
from app.modules.venue_image.schemas import VenueImageCreate, VenueImageUpdate


class VenueImageService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = BaseRepository(VenueImage, session)

    async def get_all(self, page: int, size: int) -> PaginatedResponse:
        items = await self.repo.get_all(limit=size, offset=(page - 1) * size)
        total = await self.repo.count()
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            total_pages=(total + size - 1) // size,
        )

    async def get_by_id(self, id: uuid.UUID) -> VenueImage:
        obj = await self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=404, detail="VenueImage not found")
        return obj

    async def create(self, data: VenueImageCreate) -> VenueImage:
        return await self.repo.create(**data.model_dump())

    async def update(self, id: uuid.UUID, data: VenueImageUpdate) -> VenueImage:
        obj = await self.get_by_id(id)
        return await self.repo.update(obj, **data.model_dump(exclude_none=True))

    async def delete(self, id: uuid.UUID) -> None:
        obj = await self.get_by_id(id)
        await self.repo.delete(obj)
