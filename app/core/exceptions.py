class AppException(Exception):
    status_code: int = 500
    default_detail: str = "An error occurred"
    default_code: str = "error"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.default_detail
        self.code = self.default_code


class NotFoundError(AppException):
    status_code = 404
    default_detail = "Not found"
    default_code = "not_found"


class ConflictError(AppException):
    status_code = 409
    default_detail = "Conflict"
    default_code = "conflict"


class BadRequestError(AppException):
    status_code = 400
    default_detail = "Bad request"
    default_code = "bad_request"


class ForbiddenError(AppException):
    status_code = 403
    default_detail = "Forbidden"
    default_code = "forbidden"


class UnauthorizedError(AppException):
    status_code = 401
    default_detail = "Unauthorized"
    default_code = "unauthorized"
