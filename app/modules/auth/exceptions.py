from app.core.exceptions import AppException


class GoogleAuthError(AppException):
    status_code = 401
    default_detail = "Google authentication failed"
    default_code = "google_auth_failed"
