from src.models.facilities import FacilitiesOrm
from src.repo.base import BaseRepository
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
