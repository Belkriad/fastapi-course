import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()
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


class HotelSchema(BaseModel):
    title: str
    name: str


class HotelUpdate(BaseModel):
    title: str | None = None
    name: str | None = None


def check_hotel_by_id(hotel_id: int, hotels: list[dict[str]]):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            return
    raise HTTPException(status_code=404, detail="Id hotel not found")


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),
    page: int = Query(1),
    per_page: int = Query(3),
):
    if per_page < 1 or page < 1:
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
    num_rec = count_hotels if per_page > count_hotels else per_page
    max_page = count_hotels // num_rec
    if max_page == 1:
        return hotels_
    start = (page - 1) * num_rec if page <= max_page else (max_page - 1) * num_rec
    end = page * num_rec if page <= max_page else max_page * num_rec
    return hotels_[start:end]


@app.put("/hotels/{hotel_id}")
def edit_hotel(hotel_id: int, payload: HotelSchema):
    check_hotel_by_id(hotel_id, hotels)
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = payload.title
            hotel["name"] = payload.name
    return {"status": "ok"}


@app.patch("/hotels/{hotel_id}")
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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
