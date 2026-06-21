from app.core.exceptions import NotFoundError


class OrderItemNotFoundError(NotFoundError):
    default_detail = "Order item not found"
    default_code = "order_item_not_found"
