from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repo.rooms import RoomsRepository
from src.schemas.rooms import RoomSchema

router = APIRouter(prefix="/rooms", tags=["Комнаты"])


@router.get("/")
async def get_rooms(
    pagination: PaginationDep,
    price: int | None = Query(None, description="Цена за номер"),
    quantity: int | None = Query(None, description="Количество номеров"),
    title: str | None = Query(None, description="Название"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            price=price,
            quantity=quantity,
            title=title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )


@router.post("")
async def create_room(
    room_data: RoomSchema = Body(
        openapi_examples={
            "1": {
                "summary": "hotel_id = 3 ",
                "value": {
                    "title": "Номер для одного",
                    "hotel_id": 3,
                    "description": "Просторная комната",
                    "price": 34990,
                    "quantity": 7,
                },
            },
            "2": {
                "summary": "hotel_id = 12",
                "value": {
                    "title": "Номер люкс",
                    "hotel_id": 12,
                    "description": "",
                    "price": 120999,
                    "quantity": 1,
                },
            },
        }
    ),
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}



@router.patch("/{room_id}")
async def partially_edit_hotel(room_id: int, hotel_data: RoomSchema):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(hotel_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{room_id}")
async def edit_hotel(room_id: int, hotel_data: RoomSchema):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(hotel_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{room_id}")
async def delete_hotel(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}
