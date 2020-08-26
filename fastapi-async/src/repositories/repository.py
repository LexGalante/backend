from databases import Database


class Repository:
    def __init__(self, database: Database):
        self._database: Database = database

    async def execute(self, sql: str, parameters: list | dict = None):
        if type(parameters) is list:
            await self._database.execute_many(query=sql, values=parameters)
        else:
            await self._database.execute(query=sql, values=parameters)

    async def query(self, sql: str, parameters: dict = None):
        rows = await self._database.fetch_all(query=sql, values=parameters)

        return rows

    async def single(self, sql: str, parameters: dict = None):
        row = await self._database.fetch_one(query=sql, values=parameters)

        return row

    async def scalar(self, sql: str, parameters: dict = None):
        value = await self._database.fetch_val(query=sql, values=parameters)

        return value
