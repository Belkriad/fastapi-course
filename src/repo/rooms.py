from sqlalchemy import func, select

from src.models.rooms import RoomsOrm
from src.repo.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
        self,
        price,
        quantity,
        title,
        limit,
        offset,
    ):
        query = select(RoomsOrm)
        if price:
            query = query.filter_by(price=price)
        if quantity:
            query = query.filter_by(quantity=quantity)
        if title:
            query = query.filter(
                func.lower(RoomsOrm.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_price(self, room_id):
        query = select(RoomsOrm.price).filter_by(id=room_id)
        result = await self.session.execute(query)
        return result.scalar_one()
