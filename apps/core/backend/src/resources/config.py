from os import getenv

from pydantic import PostgresDsn


class Config():
    API_ENABLE_HTTPS_REDIRECT: bool = False
    API_ENABLE_CORS: bool = bool(getenv("API_ENABLE_CORS"))
    API_SECRET: str = getenv("API_SECRET", "Iggl3Secret@")

    POSTGRES_DATABASE = getenv("POSTGRES_DATABASE", "postgres")
    POSTGRES_USER = getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER = getenv("POSTGRES_SERVER", "postgres")

    def get_connection_string(self):
        return PostgresDsn.build(
            scheme=self.POSTGRES_DATABASE,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            path=f"{self.POSTGRES_DATABASE}"
        )


config = Config
