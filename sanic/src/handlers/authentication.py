from sanic.request import Request
from sanic_jwt.exceptions import AuthenticationFailed


async def authenticate(request: Request):
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        raise AuthenticationFailed("Missing email or password")

    pool = request.app.config['pool']
    async with pool.acquire() as connection:
        sql = "SELECT * FROM users WHERE email = $1"
        user = await connection.fetchrow(sql, email)

        if user is None:
            raise AuthenticationFailed("User not found")

        if user.get('password') not in password:
            raise AuthenticationFailed("Invalid password")

        return {'email': user.get('email')}
