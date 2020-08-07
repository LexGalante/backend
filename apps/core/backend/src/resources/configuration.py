from os import getenv


class Configuration:
    PROJECT_NAME: str = getenv("PROJECT_NAME", "Iggle-Api-Backend")
    MONGODB_URL: str = getenv("MONGODB_URL")
    MONGODB_DATABASE: str = getenv("MONGODB_DATABASE")
    MONGODB_MAX_CONNECTIONS: int = getenv("MONGODB_MAX_CONNECTIONS")
    MONGODB_MIN_CONNECTIONS: int = getenv("MONGODB_MIN_CONNECTIONS")
    ENVIROMENT: str = "development"
    ENABLE_HTTPS_REDIRECT: bool = bool(getenv("ENABLE_HTTPS_REDIRECT", False))
    ENABLE_CUSTOM_ERROR: bool = bool(getenv("ENABLE_CUSTOM_ERROR", False))


class TestingConfiguration(Configuration):
    ENVIROMENT: str = "testing"


class ReleaseConfiguration(Configuration):
    ENVIROMENT: str = "release"


def get_configuration() -> Configuration:
    """"Retrieve enviroment variables"""
    if getenv("ENVIROMENT") == "release":
        return ReleaseConfiguration()
    elif getenv("ENVIROMENT") == "testing":
        return TestingConfiguration()
    else:
        return Configuration()
