from app.core.exceptions import ConflictError, NotFoundError


class ReservationNotFoundError(NotFoundError):
    default_detail = "Reservation not found"
    default_code = "reservation_not_found"


class InvalidReservationStatusTransitionError(ConflictError):
    default_detail = "Invalid reservation status transition"
    default_code = "invalid_reservation_status_transition"
