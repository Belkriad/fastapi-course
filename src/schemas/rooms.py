from pydantic import BaseModel


class RoomSchema(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int
