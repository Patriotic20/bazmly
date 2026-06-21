import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.schemas.base import PaginatedResponse
from app.modules.order_item.schemas import OrderItemCreate, OrderItemResponse, OrderItemUpdate
from app.modules.order_item.service import OrderItemService

router = APIRouter(prefix="/order-items", tags=["order-items"])


@router.get("/", response_model=PaginatedResponse[OrderItemResponse])
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await OrderItemService(session).get_all(page, size)


@router.get("/{id}", response_model=OrderItemResponse)
async def get_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrderItemResponse:
    return await OrderItemService(session).get_by_id(id)


@router.post("/", response_model=OrderItemResponse, status_code=201)
async def create(
    data: OrderItemCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrderItemResponse:
    return await OrderItemService(session).create(data)


@router.patch("/{id}", response_model=OrderItemResponse)
async def update(
    id: uuid.UUID,
    data: OrderItemUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrderItemResponse:
    return await OrderItemService(session).update(id, data)


@router.delete("/{id}", status_code=204)
async def delete(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await OrderItemService(session).delete(id)
