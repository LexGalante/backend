from typing import List

from models.user import User
from repositories.user_repository import UserRepository
from resources.dbcontext import DbContext
from resources.security import encrypt, validate


class UserService():
    def __init__(self, dbcontext: DbContext):
        self._dbcontext: DbContext = dbcontext
        self._repository: UserRepository = UserRepository(dbcontext)

    def get_all(self, page: int, page_size: int) -> List[User]:
        return self._repository.get_all(page, page_size)

    def get_by_email(self, email: str) -> User:
        return self._repository.get_by_email(email)

    def create(self, data) -> User:
        user = User(**data)
        user.password = encrypt(user.password)
        user.active = True
        self._repository.create(user)
        self._dbcontext.commit()

        return user

    def update(self, data) -> User:
        pass

    def delete(self, data):
        pass

    def authenticate(self, email, password) -> User:
        user = self._repository.get_by_email(email)
        if user is None or not validate(password, user.password):
            raise ValueError("Invalid username or password")

        return user
