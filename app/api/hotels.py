from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.api.dependencies import PaginationDep
from app.database import async_session_maker
from app.models.hotels import HotelsOrm

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
            query = query.filter(HotelsOrm.location.like(f"%{location}%"))
        if title:
            query = query.filter(HotelsOrm.title.like(f"%{title}%"))
        query = query.limit(pagination.per_page).offset(
            pagination.per_page * (pagination.page - 1)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
