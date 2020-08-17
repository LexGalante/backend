from os import getenv


API_ENABLE_HTTPS_REDIRECT: bool = False
API_ENABLE_CORS: bool = bool(getenv("API_ENABLE_CORS"))

API_SECRET: str = getenv("API_SECRET", "Iggl3Secret@")
API_MINUTES_EXPIRE_TOKEN: int = int(getenv("API_MINUTES_EXPIRE_TOKEN", 30))

CONNECTION_STRING: str = getenv("CONNECTION_STRING", "postgresql+psycopg2://postgres:postgres@localhost/postgres")
