from os import getenv

from asyncpg import create_pool
from dotenv import load_dotenv
from sanic_jwt import Initialize

from sanic import Sanic
from sanic.log import logger
from sanic.request import Request
from sanic.response import json
from src.handlers.authentication import authenticate
from src.routes.customers import CustomerRouter

# load .env
load_dotenv()
# create sanic
app = Sanic(__name__)
# routes
app.add_route(CustomerRouter.as_view(), '/customers')
# jwt
Initialize(app, authenticate=authenticate)


@app.listener('before_server_start')
async def connect_database(app, loop):
    logger.info("Connecting database...")
    host = getenv('DB_HOST', 'localhost')
    port = getenv('DB_PORT', '5432')
    user = getenv('DB_USER', 'postgres')
    password = getenv('DB_PASSWORD', 'postgres')
    database = getenv('DB_NAME', 'postgres')
    app.config['pool'] = await create_pool(
        dsn=f"postgres://{user}:{password}@{host}:{port}/{database}",
        min_size=5,
        max_size=25,
        max_queries=50000,
        max_inactive_connection_lifetime=300,
        loop=loop
    )


@app.listener('after_server_stop')
async def disconnect_database(app, loop):
    logger.info("Disconnecting database...")
    pool = app.config['pool']
    async with pool.acquire() as conn:
        await conn.close()


@app.route("/")
async def index(request: Request):
    return json({"status": True, "message": "Welcome Sanic"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, access_log=True)
