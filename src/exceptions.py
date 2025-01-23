class MomoaException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MomoaException):
    detail = "Object not found"


class NoAvailableRoomsException(MomoaException):
    detail = "No rooms left"


class ObjectAlreadyExistsException(MomoaException):
    detail = "Object already exists"


class HotelNotFoundException(MomoaException):
    detail = "Hotel not found"
