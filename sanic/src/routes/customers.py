from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView


class CustomerRouter(HTTPMethodView):
    async def get(self, request: Request):
        pool = request.app.config['pool']
        async with pool.acquire() as connection:
            customers = await connection.fetch("SELECT * FROM customers")

            return json(customers)

    async def post(self, request: Request):
        pool = request.app.config['pool']
        async with pool.acquire() as connection:
            name = request.json.get('name')
            sql = "INSERT INTO customert(name) VALUES($1)"
            await connection.execute(sql, name)

    async def put(self, request: Request):
        pool = request.app.config['pool']
        async with pool.acquire() as connection:
            id = request.args.get('id', None)
            name = request.json.get('name')
            sql = "UPDATE customers SET name = $1 WHERE id = $2"
            await connection.execute(sql, name, id)

    async def delete(self, request: Request):
        pool = request.app.config['pool']
        async with pool.acquire() as connection:
            id = request.args.get('id', None)
            sql = "DELETE FROM customers id = $2"
            await connection.execute(sql, id)
