from os import getenv

from dotenv import load_dotenv
from sanic_jwt import Initialize
from tortoise.contrib.sanic import register_tortoise

from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from src.configurations import configuration
from src.handlers import authentication
from src.routes.customers import CustomerRouter

# load .env
load_dotenv()
# create sanic
app = Sanic(__name__)
# routes
app.add_route(CustomerRouter.as_view(), '/customers', version=1)
# jwt
Initialize(
    app,
    configuration_class=configuration.JwtConfiguration,
    authenticate=authentication.authenticate,
    retrieve_user=authentication.retrieve_user
)
# orm
register_tortoise(
    app,
    db_url=f"postgres://{getenv('DB_USER', 'postgres')}:{getenv('DB_PASSWORD', 'postgres')}@{getenv('DB_HOST', 'localhost')}:{getenv('DB_PORT', '5432')}/{getenv('DB_NAME', 'postgres')}",
    modules={
        'models': [
            'src.models.user',
            'src.models.customer',
        ]
    },
    generate_schemas=True
)


@app.route("/")
async def index(request: Request):
    return json({"status": True, "message": "Welcome Sanic"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, access_log=True)
