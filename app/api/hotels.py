from fastapi import APIRouter, Body, Query
from sqlalchemy import insert, select

from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.models.hotels import HotelsOrm
from app.schemas.hotels import HotelSchema

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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}
