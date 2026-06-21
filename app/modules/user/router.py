import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.schemas.base import PaginatedResponse
from app.modules.user.schemas import UserCreate, UserResponse
from app.modules.user.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=PaginatedResponse[UserResponse])
async def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await UserService(session).get_all(page, size)


@router.get("/{id}", response_model=UserResponse)
async def get_by_id(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserResponse:
    return await UserService(session).get_by_id(id)


@router.post("/", response_model=UserResponse, status_code=201)
async def create(
    data: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserResponse:
    return await UserService(session).create(data)


@router.delete("/{id}", status_code=204)
async def delete(
    id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await UserService(session).delete(id)
