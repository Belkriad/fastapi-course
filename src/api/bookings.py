from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep, PaginationDep, UserIdDep
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
    booking = await db.bookings.add(booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(
    pagination: PaginationDep,
    db: DBDep,
):
    per_page = pagination.per_page or 5
    return await db.bookings.get_all(
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("me")
async def get_booking_for_user(
    user_id: UserIdDep,
    db: DBDep,
):
    return await db.bookings.get_filtered(user_id=user_id)
