import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.schemas.base import PaginatedResponse
from app.modules.restaurant.schemas import RestaurantCreate, RestaurantResponse, RestaurantUpdate
from app.modules.restaurant.service import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("/", response_model=PaginatedResponse[RestaurantResponse])
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await RestaurantService(session).get_all(page, size)


@router.get("/{id}", response_model=RestaurantResponse)
async def get_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> RestaurantResponse:
    return await RestaurantService(session).get_by_id(id)


@router.post("/", response_model=RestaurantResponse, status_code=201)
async def create(
    data: RestaurantCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> RestaurantResponse:
    return await RestaurantService(session).create(data)


@router.patch("/{id}", response_model=RestaurantResponse)
async def update(
    id: uuid.UUID,
    data: RestaurantUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> RestaurantResponse:
    return await RestaurantService(session).update(id, data)


@router.delete("/{id}", status_code=204)
async def delete(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await RestaurantService(session).delete(id)
