import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.schemas.base import PaginatedResponse
from app.modules.menu_item.schemas import MenuItemCreate, MenuItemResponse, MenuItemUpdate
from app.modules.menu_item.service import MenuItemService

router = APIRouter(prefix="/menu-items", tags=["menu-items"])


@router.get("/", response_model=PaginatedResponse[MenuItemResponse])
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await MenuItemService(session).get_all(page, size)


@router.get("/{id}", response_model=MenuItemResponse)
async def get_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> MenuItemResponse:
    return await MenuItemService(session).get_by_id(id)


@router.post("/", response_model=MenuItemResponse, status_code=201)
async def create(
    data: MenuItemCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> MenuItemResponse:
    return await MenuItemService(session).create(data)


@router.patch("/{id}", response_model=MenuItemResponse)
async def update(
    id: uuid.UUID,
    data: MenuItemUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> MenuItemResponse:
    return await MenuItemService(session).update(id, data)


@router.delete("/{id}", status_code=204)
async def delete(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await MenuItemService(session).delete(id)
