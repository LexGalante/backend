from typing import List

from sqlalchemy.exc import IntegrityError

from .repository import Repository
from resources.dbcontext import DbContext
from models.user import User
from resources.logger import Logger


class UserRepository(Repository):
    def __init__(self, db: DbContext):
        super().__init__(db)

    def get_all(self, page: int, page_size: int) -> List[User]:
        return self._db.session.query(User).offset((page - 1) * page_size).limit(page_size).all()

    def get_by_id(self, id: int) -> User:
        return self._db.session.query(User).filter(id == id).first()

    def get_by_email(self, email: str) -> User:
        return self._db.session.query(User).filter(email == email).first()

    def create(self, user: User):
        self._db.session.add(user)

    def delete(self, id: int):
        self._db.session.delete(User).where(User.id == id)
