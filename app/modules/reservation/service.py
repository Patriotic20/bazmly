import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repository.base import BaseRepository
from app.core.schemas.base import PaginatedResponse
from app.modules.reservation.model import Reservation
from app.modules.reservation.schemas import ReservationCreate, ReservationUpdate


class ReservationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = BaseRepository(Reservation, session)

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

    async def get_by_id(self, id: uuid.UUID) -> Reservation:
        obj = await self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return obj

    async def create(self, data: ReservationCreate) -> Reservation:
        return await self.repo.create(**data.model_dump())

    async def update(self, id: uuid.UUID, data: ReservationUpdate) -> Reservation:
        obj = await self.get_by_id(id)
        return await self.repo.update(obj, **data.model_dump(exclude_none=True))

    async def delete(self, id: uuid.UUID) -> None:
        obj = await self.get_by_id(id)
        await self.repo.delete(obj)
