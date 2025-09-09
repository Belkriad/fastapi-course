from fastapi import APIRouter, Body, Query
from sqlalchemy import select

from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.models.hotels import HotelsOrm
from app.schemas.hotels import HotelSchema
from repo.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/hotels")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.icontains(location))
        if title:
            query = query.filter(HotelsOrm.title.icontains(title))
        query = query.limit(pagination.per_page).offset(
            pagination.per_page * (pagination.page - 1)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1),
        )


@router.post("")
async def create_hotel(
    hotel_data: HotelSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "Сочи, ул. Моря, ",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель У фонтана",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelSchema):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
