from app.core.exceptions import ConflictError, NotFoundError


class UserNotFoundError(NotFoundError):
    default_detail = "User not found"
    default_code = "user_not_found"


class UserAlreadyExistsError(ConflictError):
    default_detail = "Username already taken"
    default_code = "user_already_exists"
