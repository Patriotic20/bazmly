import uuid

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token
from app.modules.auth.exceptions import GoogleAuthError
from app.modules.auth.schemas import TokenResponse
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

        user = await self._find_or_create_user(google_id, email, name)
        return TokenResponse(access_token=create_access_token(str(user.id)))

    async def _find_or_create_user(self, google_id: str, email: str, name: str) -> User:
        result = await self.session.execute(
            select(User).where(User.google_id == google_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            username = email.split("@")[0] or name.replace(" ", "_").lower() or f"user_{uuid.uuid4().hex[:8]}"
            user = User(username=username, google_id=google_id, password=None)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        return user
