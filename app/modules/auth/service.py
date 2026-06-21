import secrets
import uuid
from datetime import datetime, timedelta, timezone

import httpx
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.email import send_verification_email
from app.core.security import create_access_token
from app.modules.auth.exceptions import (
    EmailAlreadyVerifiedError,
    GoogleAuthError,
    InvalidVerificationTokenError,
)
from app.modules.auth.schemas import TokenResponse
from app.modules.auth.verification_model import EmailVerification
from app.modules.user.exceptions import UserNotFoundError
from app.modules.user.model import User

_GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
_GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
_GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def get_google_redirect_url(self) -> str:
        params = {
            "client_id": settings.google.client_id,
            "redirect_uri": settings.google.redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{_GOOGLE_AUTH_URL}?{query}"

    async def handle_google_callback(self, code: str) -> TokenResponse:
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                _GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.google.client_id,
                    "client_secret": settings.google.client_secret,
                    "redirect_uri": settings.google.redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            if token_resp.status_code != 200:
                raise GoogleAuthError()

            access_token = token_resp.json()["access_token"]

            userinfo_resp = await client.get(
                _GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if userinfo_resp.status_code != 200:
                raise GoogleAuthError()

            userinfo = userinfo_resp.json()

        google_id: str = userinfo["id"]
        email: str = userinfo.get("email", "")
        name: str = userinfo.get("name", "")

        user = await self._find_or_create_google_user(google_id, email, name)
        return TokenResponse(access_token=create_access_token(str(user.id)))

    async def _find_or_create_google_user(self, google_id: str, email: str, name: str) -> User:
        result = await self.session.execute(
            select(User).where(User.google_id == google_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            username = (
                email.split("@")[0]
                or name.replace(" ", "_").lower()
                or f"user_{uuid.uuid4().hex[:8]}"
            )
            user = User(
                username=username,
                email=email,
                google_id=google_id,
                password=None,
                is_verified=True,
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        return user

    async def verify_email(self, token: str) -> None:
        result = await self.session.execute(
            select(EmailVerification).where(EmailVerification.token == token)
        )
        verification = result.scalar_one_or_none()

        if verification is None:
            raise InvalidVerificationTokenError()
        if verification.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            await self.session.delete(verification)
            await self.session.commit()
            raise InvalidVerificationTokenError("Verification token has expired")

        user = await self.session.get(User, verification.user_id)
        if user is not None:
            user.is_verified = True

        await self.session.delete(verification)
        await self.session.commit()

    async def resend_verification(self, email: str) -> None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFoundError()
        if user.is_verified:
            raise EmailAlreadyVerifiedError()

        await self.session.execute(
            delete(EmailVerification).where(EmailVerification.user_id == user.id)
        )

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        verification = EmailVerification(user_id=user.id, token=token, expires_at=expires_at)
        self.session.add(verification)
        await self.session.commit()

        send_verification_email(email, token)
