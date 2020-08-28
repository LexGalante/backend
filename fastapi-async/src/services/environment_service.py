import logging
from typing import List
from databases import Database

from resources.database import environments


class EnvironmentService:
    def __init__(self, database: Database):
        self._database: Database = database
        self._logger = logging.getLogger(__name__)

    async def get_all(self) -> List[dict]:
        return await self._database.fetch_all(query=environments.select())

    async def get_by_name(self, name: str):
        sql = "SELECT * FROM environments WHERE name = :name"
        parameters = {"name": name}
        return await self._database.fetch_one(query=sql, values=parameters)
