from app.core.exceptions import ConflictError, NotFoundError


class OrderNotFoundError(NotFoundError):
    default_detail = "Order not found"
    default_code = "order_not_found"


class InvalidOrderStatusTransitionError(ConflictError):
    default_detail = "Invalid order status transition"
    default_code = "invalid_order_status_transition"
