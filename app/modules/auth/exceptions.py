from app.core.exceptions import AppException, BadRequestError, ConflictError, ForbiddenError


class GoogleAuthError(AppException):
    status_code = 401
    default_detail = "Google authentication failed"
    default_code = "google_auth_failed"


class InvalidVerificationTokenError(BadRequestError):
    default_detail = "Verification token is invalid or expired"
    default_code = "invalid_verification_token"


class EmailAlreadyVerifiedError(ConflictError):
    default_detail = "Email is already verified"
    default_code = "email_already_verified"


class AccountNotVerifiedError(ForbiddenError):
    default_detail = "Please verify your email before using the API"
    default_code = "account_not_verified"
