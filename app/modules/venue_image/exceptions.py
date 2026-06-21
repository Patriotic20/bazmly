from app.core.exceptions import NotFoundError


class VenueImageNotFoundError(NotFoundError):
    default_detail = "Venue image not found"
    default_code = "venue_image_not_found"
