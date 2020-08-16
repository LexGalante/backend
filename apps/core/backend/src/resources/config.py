from os import get_env


class Config():
    API_ENABLE_HTTPS_REDIRECT: bool = get_env("API_ENABLE_HTTPS_REDIRECT", False)
    API_ENABLE_CORS: bool = get_env("API_ENABLE_CORS", True)
    API_SECRET: str = get_env("API_SECRET", "Iggl3Secret@")

    CONNECTION_STRING: str = get_env("CONNECTION_STRING", "postgresql+psycopg2://postgres:postgres@postgres/postgres")


config = Config
