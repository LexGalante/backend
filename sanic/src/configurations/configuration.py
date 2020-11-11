from os import getenv

from sanic_jwt import Configuration


class JwtConfiguration(Configuration):
    secret = getenv('JWT_SECRET', 'M3uS3gr3d0Sup3rS3cr3t0')
    expiration_delta = int(getenv('JWT_MINUTES_TO_EXPIRE', 30))
    user_id = 'email'
