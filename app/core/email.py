import resend

from app.core.config import settings


def send_verification_email(to_email: str, token: str) -> None:
    resend.api_key = settings.resend.api_key
    verify_url = f"http://localhost:8000/api/v1/auth/verify-email?token={token}"
    resend.Emails.send({
        "from": settings.resend.from_email,
        "to": [to_email],
        "subject": "Verify your Bazmly account",
        "html": (
            f"<h2>Welcome to Bazmly!</h2>"
            f"<p>Click the button below to verify your email address. "
            f"This link expires in 24 hours.</p>"
            f'<a href="{verify_url}" style="display:inline-block;padding:12px 24px;'
            f'background:#1a73e8;color:#fff;text-decoration:none;border-radius:6px;">'
            f"Verify Email</a>"
            f"<p>Or copy this link: {verify_url}</p>"
        ),
    })
