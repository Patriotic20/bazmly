from app.core.exceptions import ConflictError, NotFoundError


class ReviewNotFoundError(NotFoundError):
    default_detail = "Review not found"
    default_code = "review_not_found"


class ReviewAlreadyExistsError(ConflictError):
    default_detail = "You have already reviewed this restaurant"
    default_code = "review_already_exists"
