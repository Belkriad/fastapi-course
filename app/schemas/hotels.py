from pydantic import BaseModel


class HotelSchema(BaseModel):
    title: str
    name: str


class HotelUpdate(BaseModel):
    title: str | None = None
    name: str | None = None
