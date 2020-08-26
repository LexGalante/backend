from typing import List
from databases import Database

from .repository import Repository
from tables.application import applications


class ApplicationRepository(Repository):
    def __init__(self, database: Database):
        super().__init__(database)

    async def get_all_by_user(self, user: dict) -> List[dict]:
        sql = """SELECT a.* FROM applications a 
                LEFT JOIN application_users au ON a.id = au.application_id
                LEFT JOIN users u ON au.user_id = u.id 
                WHERE u.email = :email"""
        return await self.query(sql, {"email": user["email"]})

    async def get_by_name(self, name: str, user: dict) -> dict:
        sql = """SELECT a.* FROM applications a 
                LEFT JOIN application_users au ON a.id = au.application_id
                LEFT JOIN users u ON au.user_id = u.id 
                WHERE u.email = :email
                AND a.name = :application"""
        return await self.query(sql, {"email": user["email"], "application": name})

    async def create(self, application: dict):
        sql = applications.insert().value(
            name=application["name"],
            real_name=application["real_name"],
            model=application["model"],
            description=application["description"],
            details=application["details"],
            active=application["active"],
            created_at=application["created_at"],
            created_by=application["created_by"],
            updated_at=application["updated_at"],
            updated_by=application["updated_by"]
        )
        await self.execute(sql)

    async def name_exists(self, name: str) -> bool:
        try:
            sql = "SELECT COUNT(*) FROM applications WHERE name = :name"
            count = await self.scalar(sql)

            return int(count) > 0
        except ValueError:
            return False
