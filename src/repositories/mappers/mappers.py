from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import BookingDTO
from src.schemas.facilities import FacilityDTO, RoomFacilityDTO
from src.schemas.hotels import HotelDTO
from src.schemas.rooms import RoomDTO, RoomWithRelsDTO
from src.schemas.users import UserDTO, UserWithHashedPasswordDTO


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = HotelDTO


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomDTO


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRelsDTO


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserDTO


class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserWithHashedPasswordDTO


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = BookingDTO


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = FacilityDTO


class RoomsFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomFacilityDTO
