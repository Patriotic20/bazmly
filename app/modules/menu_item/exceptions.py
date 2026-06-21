from app.core.exceptions import NotFoundError


class MenuItemNotFoundError(NotFoundError):
    default_detail = "Menu item not found"
    default_code = "menu_item_not_found"
