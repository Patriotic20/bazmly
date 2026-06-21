from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.menu_item.router import router as menu_item_router
from app.modules.order.router import router as order_router
from app.modules.order_item.router import router as order_item_router
from app.modules.reservation.router import router as reservation_router
from app.modules.restaurant.router import router as restaurant_router
from app.modules.review.router import router as review_router
from app.modules.user.router import router as user_router
from app.modules.venue_image.router import router as venue_image_router


PREFIX = "/api/v1"

router = APIRouter()

router.include_router(auth_router, prefix=PREFIX)
router.include_router(user_router, prefix=PREFIX)
router.include_router(restaurant_router, prefix=PREFIX)
router.include_router(menu_item_router, prefix=PREFIX)
router.include_router(order_router, prefix=PREFIX)
router.include_router(order_item_router, prefix=PREFIX)
router.include_router(reservation_router, prefix=PREFIX)
router.include_router(review_router, prefix=PREFIX)
router.include_router(venue_image_router, prefix=PREFIX)
