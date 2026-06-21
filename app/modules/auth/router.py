from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import db_helper
from app.modules.auth.schemas import ResendVerificationRequest, TokenResponse
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google")
async def google_login() -> RedirectResponse:
    url = AuthService(None).get_google_redirect_url()
    return RedirectResponse(url)


@router.get("/google/callback")
async def google_callback(
    code: str,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> RedirectResponse:
    result = await AuthService(session).handle_google_callback(code)
    return RedirectResponse(f"/test#token={result.access_token}")


@router.get("/verify-email")
async def verify_email(
    token: str,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> dict:
    await AuthService(session).verify_email(token)
    return {"message": "Email verified successfully"}


@router.post("/resend-verification")
async def resend_verification(
    data: ResendVerificationRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> dict:
    await AuthService(session).resend_verification(data.email)
    return {"message": "Verification email sent"}
