import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()
hotels = [
    {"id": 1, "title": "Sochi", "name": "Сочи"},
    {"id": 2, "title": "Dubai", "name": "Дубай"},
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
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


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
