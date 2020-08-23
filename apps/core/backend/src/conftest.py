from typing import Generator

import pytest
from fastapi.testclient import TestClient

from main import app
from resources.dbcontext import DbContext


@pytest.fixture(scope="module")
def http_client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def dbcontext() -> Generator:
    yield DbContext()

