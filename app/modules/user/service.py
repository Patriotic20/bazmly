import secrets
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.email import send_verification_email
from app.core.repository.base import BaseRepository
from app.core.schemas.base import PaginatedResponse
from app.modules.auth.verification_model import EmailVerification
from app.modules.user.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.modules.user.model import User
from app.modules.user.schemas import UserCreate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = BaseRepository(User, session)
        self.session = session

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

    async def get_by_id(self, id: uuid.UUID) -> User:
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise UserNotFoundError()
        return obj

    async def create(self, data: UserCreate) -> User:
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
        try:
            user = await self.repo.create(
                username=data.username,
                email=data.email,
                password=hashed,
                is_verified=False,
            )
        except IntegrityError:
            raise UserAlreadyExistsError()

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        verification = EmailVerification(user_id=user.id, token=token, expires_at=expires_at)
        self.session.add(verification)
        await self.session.commit()

        send_verification_email(data.email, token)
        return user

    async def delete(self, id: uuid.UUID) -> None:
        obj = await self.get_by_id(id)
        await self.repo.delete(obj)
