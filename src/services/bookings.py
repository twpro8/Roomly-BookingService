from src.exceptions import ObjectNotFoundException, RoomNotFoundException, BookingNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd, Booking
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, user_id: int, booking_data: BookingAddRequest) -> Booking:
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
        await self.db.commit()

        return booking

    async def delete_booking(self, user_id: int, booking_id: int) -> None:
        try:
            await self.db.bookings.get_one(id=booking_id, user_id=user_id)
        except ObjectNotFoundException:
            raise BookingNotFoundException
        await self.db.bookings.delete(id=booking_id, user_id=user_id)
        await self.db.commit()
