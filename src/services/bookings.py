from src.exceptions import (
    ObjectNotFoundException,
    RoomNotFoundException,
    BookingNotFoundException,
    HotelNotFoundException,
    NoAvailableRoomsException,
)
from src.schemas.bookings import BookingAddRequestDTO, BookingAddDTO, BookingDTO
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, user_id: int, booking_data: BookingAddRequestDTO) -> BookingDTO:
        try:
            await self.db.hotels.get_hotel(id=booking_data.hotel_id)
            room = await self.db.rooms.get_room(
                id=booking_data.room_id, hotel_id=booking_data.hotel_id
            )
            new_data = BookingAddDTO(
                user_id=user_id,
                room_id=booking_data.room_id,
                date_from=booking_data.date_from,
                date_to=booking_data.date_to,
                price=room.price,
            )
            booking = await self.db.bookings.add_booking(new_data, hotel_id=booking_data.hotel_id)
        except HotelNotFoundException:
            raise HotelNotFoundException
        except RoomNotFoundException:
            raise RoomNotFoundException
        except NoAvailableRoomsException:
            raise NoAvailableRoomsException

        await self.db.commit()
        return booking

    async def delete_booking(self, user_id: int, booking_id: int) -> None:
        try:
            await self.db.bookings.get_one(id=booking_id, user_id=user_id)
        except ObjectNotFoundException:
            raise BookingNotFoundException
        await self.db.bookings.delete(id=booking_id, user_id=user_id)
        await self.db.commit()
