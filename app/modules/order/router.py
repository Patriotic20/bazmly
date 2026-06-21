import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.schemas.base import PaginatedResponse
from app.modules.order.schemas import OrderCreate, OrderResponse, OrderUpdate
from app.modules.order.service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=PaginatedResponse[OrderResponse])
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await OrderService(session).get_all(page, size)


@router.get("/{id}", response_model=OrderResponse)
async def get_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrderResponse:
    return await OrderService(session).get_by_id(id)


@router.post("/", response_model=OrderResponse, status_code=201)
async def create(
    data: OrderCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrderResponse:
    return await OrderService(session).create(data)


@router.patch("/{id}", response_model=OrderResponse)
async def update(
    id: uuid.UUID,
    data: OrderUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrderResponse:
    return await OrderService(session).update(id, data)


@router.delete("/{id}", status_code=204)
async def delete(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await OrderService(session).delete(id)
