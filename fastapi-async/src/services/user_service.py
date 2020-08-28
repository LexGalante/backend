import logging
from typing import List
from databases import Database

from resources.security import encrypt
from resources.database import users


class UserService:
    def __init__(self, database: Database):
        self._database: Database = database
        self._logger = logging.getLogger(__name__)

    async def get_all(self, page: int, page_size: int) -> List[dict]:
        sql = "SELECT * FROM users OFFSET :offset LIMIT :limit"
        parameters = {"offset": ((page - 1) * page_size), "limit": page_size}
        users = await self._database.fetch_all(query=sql, values=parameters)

        return users

    async def get_by_email(self, email: str) -> dict:
        sql = "SELECT * FROM users WHERE email = :email"
        parameters = {"email": email}
        user = await self._database.fetch_one(sql, parameters)

        return user

    async def get_user_id_by_email(self, email) -> int:
        sql = "SELECT id FROM users WHERE email = :email"
        parameters = {"email": email}
        return await self._database.fetch_val(query=sql, values=parameters)

    async def create(self, user):
        if "active" not in user.keys():
            user["active"] = True
        sql = users.insert().values(
            email=user["email"],
            password=encrypt(user["password"]),
            active=user["active"]
        )
        await self._database.execute(query=sql)

    async def activate(self, email: str):
        await self.toggle_active(email, True)

    async def inactivate(self, email: str):
        await self.toggle_active(email, False)

    async def toggle_active(self, email: str, status: bool):
        sql = users.update().where(users.c.email == email).values(active=status)
        await self._database.execute(query=sql)

    async def change_password(self, email: str, new_password: str, confirm_password: str):
        if new_password != confirm_password:
            raise ValueError("password assword confirmation is invalid")
        sql = users.update().where(users.c.email == email).values(password=encrypt(new_password))
        await self._database.execute(query=sql)


