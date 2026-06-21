import uuid

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.modules.auth.exceptions import AccountNotVerifiedError
from app.modules.user.exceptions import UserNotFoundError
from app.modules.user.model import User

bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
        user_id: str = payload["sub"]
    except (JWTError, KeyError):
        raise UnauthorizedError()

    user = await session.get(User, uuid.UUID(user_id))
    if user is None:
        raise UserNotFoundError()
    if not user.is_verified:
        raise AccountNotVerifiedError()
    return user
