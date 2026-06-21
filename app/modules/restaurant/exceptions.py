from app.core.exceptions import NotFoundError


class RestaurantNotFoundError(NotFoundError):
    default_detail = "Restaurant not found"
    default_code = "restaurant_not_found"
