import logging

from motor.motor_asyncio import AsyncIOMotorClient

from .configuration import get_configuration

db: AsyncIOMotorClient = None
config = get_configuration()


async def get_database() -> AsyncIOMotorClient:
    return db


async def connect_database(**kwargs):
    logging.info("Database connecting...")
    try:
        config = get_configuration()
        db = AsyncIOMotorClient(config.MONGODB_URL,
                                maxPoolSize=config.MONGODB_MAX_CONNECTIONS,
                                minPoolSize=config.MONGODB_MIN_CONNECTIONS)
        if "returnInstance" in kwargs.keys() and kwargs.get("returnInstance"):
            return db
    except Exception as e:
        logging.exception(f"Error on connecting database: {str(e)}")
    else:
        logging.info("Database connecting...")


async def close_database():
    logging.info("Database disconnecting...")
    try:
        db.close()
    except Exception as e:
        logging.exception(f"Error on disconnect database: {str(e)}")
    else:
        logging.info("Database disconnecting...")


async def find(collection_name: str, query: dict):
    if collection_name is None or collection_name == "":
        return ValueError("collection_name is mandatory")

    return await db[config.MONGODB_DATABASE][collection_name].find(query)


async def find_one(collection_name: str, query: dict):
    if collection_name is None or collection_name == "":
        return ValueError("collection_name is mandatory")

    return await db[config.MONGODB_DATABASE][collection_name].find_one(query)


async def insert(collection_name: str, query: dict):
    if collection_name is None or collection_name == "":
        return ValueError("collection_name is mandatory")

    return await db[config.MONGODB_DATABASE][collection_name].insert(query)


async def insert_one(collection_name: str, query: dict):
    if collection_name is None or collection_name == "":
        return ValueError("collection_name is mandatory")

    return await db[config.MONGODB_DATABASE][collection_name].insert_one(query)


async def update(collection_name: str, query: dict):
    if collection_name is None or collection_name == "":
        return ValueError("collection_name is mandatory")

    return await db[config.MONGODB_DATABASE][collection_name].update(query)
