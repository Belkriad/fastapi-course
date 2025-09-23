from app.repo.base import BaseRepository
from app.models.users import UsersOrm
from app.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
