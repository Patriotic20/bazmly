import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repository.base import BaseRepository
from app.core.schemas.base import PaginatedResponse
from app.modules.menu_item.exceptions import MenuItemNotFoundError
from app.modules.menu_item.model import MenuItem
from app.modules.menu_item.schemas import MenuItemCreate, MenuItemUpdate


class MenuItemService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = BaseRepository(MenuItem, session)

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

    async def get_by_id(self, id: uuid.UUID) -> MenuItem:
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise MenuItemNotFoundError()
        return obj

    async def create(self, data: MenuItemCreate) -> MenuItem:
        return await self.repo.create(**data.model_dump())

    async def update(self, id: uuid.UUID, data: MenuItemUpdate) -> MenuItem:
        obj = await self.get_by_id(id)
        return await self.repo.update(obj, **data.model_dump(exclude_none=True))

    async def delete(self, id: uuid.UUID) -> None:
        obj = await self.get_by_id(id)
        await self.repo.delete(obj)
