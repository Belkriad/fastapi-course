from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(
    data: BookingAddRequest,
    user_id: UserIdDep,
    db: DBDep,
):
    price = await db.rooms.get_price(data.room_id)
    booking_data = BookingAdd(price=price, user_id=user_id, **data.model_dump())
    print(booking_data)
    booking = await db.bookings.add(booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
