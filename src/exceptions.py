from datetime import date

from fastapi.exceptions import HTTPException


class MomoaException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MomoaException):
    detail = "Object not found"


class BookingNotFoundException(ObjectNotFoundException):
    detail = "Booking not found"


class FacilityNotFoundException(ObjectNotFoundException):
    detail = "Facility not found"


class NoAvailableRoomsException(MomoaException):
    detail = "No rooms left"


class ObjectAlreadyExistsException(MomoaException):
    detail = "Object already exists"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found"


class RoomAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Room already exists"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Room not found"


class HotelAlreadyExistsException(MomoaException):
    detail = "Hotel already exists"


class UsernameAlreadyExistsException(MomoaException):
    detail = "Username already exists"


class EmailAlreadyExistsException(MomoaException):
    detail = "Email already exists"


class ImageTooLargeException(MomoaException):
    detail = "Image too large"


class UnsupportedImageFormatException(MomoaException):
    detail = "Unsupported image format"


class MomoaHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(MomoaHTTPException):
    status_code = 404
    detail = "Hotel not found"


class HotelAlreadyExistsHTTPException(MomoaHTTPException):
    status_code = 409
    detail = "Hotel with such title and location already exists"


class UserAlreadyExistsHTTPException(MomoaHTTPException):
    status_code = 409
    detail = "User with the provided email or username already exists"


class UserDoesNotExistHTTPException(MomoaHTTPException):
    status_code = 401
    detail = "User does not exist"


class IncorrectPasswordHTTPException(MomoaHTTPException):
    status_code = 401
    detail = "Incorrect password"


class RoomNotFoundHTTPException(MomoaHTTPException):
    status_code = 404
    detail = "Room not found"


class NoAvailableRoomsHTTPException(MomoaHTTPException):
    status_code = 409
    detail = "No rooms left"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422,
            detail='"Check-out" date must be later than the "check-in" date.',
        )


class UserAlreadyExistsException(MomoaException):
    detail = "User already exists"


class UserDoesNotExistException(MomoaException):
    detail = "User does not exist"


class IncorrectPasswordException(MomoaException):
    detail = "Incorrect password"


class UsernameAlreadyExistsHTTPException(MomoaHTTPException):
    status_code = 409
    detail = "User with the provided username already exists"


class EmailAlreadyExistsHTTPException(MomoaHTTPException):
    status_code = 409
    detail = "User with the provided email already exists"


class RoomAlreadyExistsHTTPException(MomoaHTTPException):
    status_code = 409
    detail = "Room with the provided title already exists"


class FacilityNotFoundHTTPException(MomoaHTTPException):
    status_code = 404
    detail = "Facility not found"


class BookingNotFoundHTTPException(MomoaHTTPException):
    status_code = 404
    detail = "Booking not found"


class ImageTooLargeHTTPException(MomoaHTTPException):
    status_code = 413
    detail = "Image too large. Max size cannot be greater than 5 MB"


class UnsupportedImageFormatHTTPException(MomoaHTTPException):
    detail = "Unsupported image format. Required Jpeg or PNG only."
    status_code = 415
