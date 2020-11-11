from sanic.request import Request
from sanic.response import empty, json
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import inject_user, protected
from src.models.customer import Customer
from src.models.user import User


class CustomerRouter(HTTPMethodView):
    decorators = [protected(), inject_user()]

    async def get(self, request: Request, user: User):
        customers = await Customer.all()

        return json([customer.dict() for customer in customers])

    async def post(self, request: Request, user: User):
        customer = Customer(**request.json)
        await customer.save()

        return json(customer.dict(), status=201)

    async def put(self, request: Request, user: User):
        customer = await Customer.filter(id=request.args.get('id', None)).first()
        if customer is None:
            return empty(status=404)
        customer.name = request.json.get('name', customer.name)
        await customer.save()

        return json(customer.dict())

    async def delete(self, request: Request, user: User):
        customer = await Customer.filter(id=request.args.get('id', None)).first()
        if customer is None:
            return empty(status=404)
        await customer.delete()

        return empty()
