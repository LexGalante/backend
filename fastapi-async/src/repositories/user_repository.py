from typing import List
from databases import Database

from .repository import Repository
from tables.users import users


class UserRepository(Repository):
    def __init__(self, database: Database):
        super().__init__(database)

    async def get_all(self, page: int, page_size: int) -> List[dict]:
        return await self.query(
            "SELECT * FROM users LIMIT :limit OFFSET :offset",
            {"limit": page_size, "offset": ((page - 1) * page_size)})

    async def get_by_id(self, id: int) -> dict:
        return await self.single("SELECT * FROM users WHERE id = :id", {"id": id})

    async def get_by_email(self, email: str) -> dict:
        return await self.single("SELECT * FROM users WHERE email = :email", {"email": email})

    async def create(self, user: dict):
        sql = users.insert().values(
            email=user["email"],
            password=user["password"],
            active=user["active"]
        )
        await self.execute(sql)

    async def delete(self, id: int):
        sql = users.delete().values(id=id)
        await self.execute(sql)
