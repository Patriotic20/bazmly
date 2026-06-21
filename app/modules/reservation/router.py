import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.schemas.base import PaginatedResponse
from app.modules.reservation.schemas import ReservationCreate, ReservationResponse, ReservationUpdate
from app.modules.reservation.service import ReservationService

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("/", response_model=PaginatedResponse[ReservationResponse])
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await ReservationService(session).get_all(page, size)


@router.get("/{id}", response_model=ReservationResponse)
async def get_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ReservationResponse:
    return await ReservationService(session).get_by_id(id)


@router.post("/", response_model=ReservationResponse, status_code=201)
async def create(
    data: ReservationCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ReservationResponse:
    return await ReservationService(session).create(data)


@router.patch("/{id}", response_model=ReservationResponse)
async def update(
    id: uuid.UUID,
    data: ReservationUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ReservationResponse:
    return await ReservationService(session).update(id, data)


@router.delete("/{id}", status_code=204)
async def delete(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await ReservationService(session).delete(id)
