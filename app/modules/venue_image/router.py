import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.schemas.base import PaginatedResponse
from app.modules.venue_image.schemas import VenueImageCreate, VenueImageResponse, VenueImageUpdate
from app.modules.venue_image.service import VenueImageService

router = APIRouter(prefix="/venue-images", tags=["venue-images"])


@router.get("/", response_model=PaginatedResponse[VenueImageResponse])
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await VenueImageService(session).get_all(page, size)


@router.get("/{id}", response_model=VenueImageResponse)
async def get_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> VenueImageResponse:
    return await VenueImageService(session).get_by_id(id)


@router.post("/", response_model=VenueImageResponse, status_code=201)
async def create(
    data: VenueImageCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> VenueImageResponse:
    return await VenueImageService(session).create(data)


@router.patch("/{id}", response_model=VenueImageResponse)
async def update(
    id: uuid.UUID,
    data: VenueImageUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> VenueImageResponse:
    return await VenueImageService(session).update(id, data)


@router.delete("/{id}", status_code=204)
async def delete(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await VenueImageService(session).delete(id)
