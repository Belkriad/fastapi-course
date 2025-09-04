from typing import Any
from fastapi import APIRouter, HTTPException, Query

from app.api.dependencies import PaginationDep
from app.schemas.hotels import HotelSchema, HotelUpdate

router = APIRouter(prefix="/hotels", tags=["Отели"])
hotels = [
    {"id": 1, "title": "Sochi", "name": "Сочи"},
    {"id": 2, "title": "Dubai", "name": "Дубай"},
    {"id": 3, "title": "Moscow", "name": "Москва"},
    {"id": 4, "title": "SaintPetersburg", "name": "Санкт-Петербург"},
    {"id": 5, "title": "Kazan", "name": "Казань"},
    {"id": 6, "title": "Anapa", "name": "Анапа"},
    {"id": 7, "title": "Gelendzhik", "name": "Геленджик"},
    {"id": 8, "title": "Yalta", "name": "Ялта"},
    {"id": 9, "title": "Novosibirsk", "name": "Новосибирск"},
    {"id": 10, "title": "Vladivostok", "name": "Владивосток"},
    {"id": 11, "title": "Rostov", "name": "Ростов-на-Дону"},
    {"id": 12, "title": "Kaliningrad", "name": "Калининград"},
]


def check_hotel_by_id(hotel_id: int, hotels: list[dict[str, Any]]):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            return
    raise HTTPException(status_code=404, detail="Id hotel not found")


@router.get("/hotels")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),
):
    if pagination.per_page < 1 or pagination.page < 1:
        raise HTTPException(
            status_code=422, detail="Negative pagination parameters are set"
        )
    hotels_ = []
    global hotels
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    count_hotels = len(hotels_)
    if count_hotels == 0:
        return []
    num_rec = count_hotels if pagination.per_page > count_hotels else pagination.per_page
    max_page = count_hotels // num_rec
    if max_page == 1:
        return hotels_
    start = (
        (pagination.page - 1) * num_rec
        if pagination.page <= max_page
        else (max_page - 1) * num_rec
    )
    end = pagination.page * num_rec if pagination.page <= max_page else max_page * num_rec
    return hotels_[start:end]


@router.put("/hotels/{hotel_id}")
def edit_hotel(hotel_id: int, payload: HotelSchema):
    check_hotel_by_id(hotel_id, hotels)
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = payload.title
            hotel["name"] = payload.name
    return {"status": "ok"}


@router.patch("/hotels/{hotel_id}")
def update_hotel(hotel_id: int, payload: HotelUpdate):
    if not payload.title and not payload.name:
        raise HTTPException(
            status_code=422, detail="The parameters for the update were not found"
        )
    check_hotel_by_id(hotel_id, hotels)
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if payload.title:
                hotel["title"] = payload.title
            if payload.name:
                hotel["name"] = payload.name
    return {"status": "ok"}
