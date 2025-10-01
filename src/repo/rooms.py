from sqlalchemy import func, select

from src.models.rooms import RoomsOrm
from src.repo.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm

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
