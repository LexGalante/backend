from typing import List

from models.user import User
from repositories.user_repository import UserRepository
from resources.dbcontext import DbContext


class UserService():
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def get_all(self, page: int, page_size: int) -> List[User]:
        return self._repository.get_all(page, page_size)

    def get_by_email(self, email: str) -> User:
        return self._repository.get_by_email(email)


