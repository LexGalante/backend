from databases import Database

from .config import CONNECTION_STRING, MIN_CONNECTIONS, MAX_CONNECTIONS


database: Database = Database(CONNECTION_STRING, min_size=MIN_CONNECTIONS, max_size=MAX_CONNECTIONS)


async def database_connect():
    await database.connect()


async def database_disconnect():
    await database.disconnect()


