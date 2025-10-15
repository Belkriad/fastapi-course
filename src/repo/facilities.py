from sqlalchemy import and_, select

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repo.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def edit_facilities(self, data: list[int], room_id: int):
        result = await self.session.execute(
            select(self.model.facility_id).filter_by(room_id=room_id)
        )
        id_db = set(result.scalars().all())
        id_data = set(data)
        id_del = list(id_db - id_data)
        id_add = list(id_data - id_db)
        if id_add:
            rooms_facilities_data = [
                RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in id_add
            ]
            await self.add_bulk(rooms_facilities_data)
        if id_del:
            await self.delete_bulk(
                and_(self.model.facility_id.in_(id_del), self.model.room_id == room_id)
            )
        return
