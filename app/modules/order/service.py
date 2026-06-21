import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repository.base import BaseRepository
from app.core.schemas.base import PaginatedResponse
from app.modules.order.enums import OrderStatus
from app.modules.order.exceptions import InvalidOrderStatusTransitionError, OrderNotFoundError
from app.modules.order.model import Order
from app.modules.order.schemas import OrderCreate, OrderUpdate

_VALID_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.COMPLETED, OrderStatus.CANCELLED},
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELLED: set(),
}


class OrderService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = BaseRepository(Order, session)

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

    async def get_by_id(self, id: uuid.UUID) -> Order:
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise OrderNotFoundError()
        return obj

    async def create(self, data: OrderCreate) -> Order:
        return await self.repo.create(**data.model_dump())

    async def update(self, id: uuid.UUID, data: OrderUpdate) -> Order:
        obj = await self.get_by_id(id)
        if data.status is not None and data.status not in _VALID_TRANSITIONS[obj.status]:
            raise InvalidOrderStatusTransitionError()
        return await self.repo.update(obj, **data.model_dump(exclude_none=True))

    async def delete(self, id: uuid.UUID) -> None:
        obj = await self.get_by_id(id)
        await self.repo.delete(obj)
