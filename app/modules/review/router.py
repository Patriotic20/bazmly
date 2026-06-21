import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.schemas.base import PaginatedResponse
from app.modules.review.schemas import ReviewCreate, ReviewResponse, ReviewUpdate
from app.modules.review.service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=PaginatedResponse[ReviewResponse])
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await ReviewService(session).get_all(page, size)


@router.get("/{id}", response_model=ReviewResponse)
async def get_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ReviewResponse:
    return await ReviewService(session).get_by_id(id)


@router.post("/", response_model=ReviewResponse, status_code=201)
async def create(
    data: ReviewCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ReviewResponse:
    return await ReviewService(session).create(data)


@router.patch("/{id}", response_model=ReviewResponse)
async def update(
    id: uuid.UUID,
    data: ReviewUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> ReviewResponse:
    return await ReviewService(session).update(id, data)


@router.delete("/{id}", status_code=204)
async def delete(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await ReviewService(session).delete(id)
