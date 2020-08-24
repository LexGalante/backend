import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from alembic import command
from alembic.config import Config

from main import app
from resources.dbcontext import DbContext
from api.v1.dependency_injection import get_dbcontext

load_dotenv()


def pytest_sessionstart(session):
    os.environ["ENVIRONMENT"] = "testing"
    config = Config("alembic.ini")
    command.upgrade(config, "head")


def pytest_sessionfinish(session, exitstatus):
    os.environ["ENVIRONMENT"] = "development"


def override_get_dbcontext():
    try:
        dbcontext = DbContext(in_testing=True)
        yield dbcontext
    finally:
        dbcontext.finish()


app.dependency_overrides[get_dbcontext] = override_get_dbcontext


@pytest.fixture(scope="session")
def http_client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def http_client_authenticated() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def testing_dbcontext() -> Generator:
    dbcontext: DbContext = DbContext(in_testing=True)
    try:
        dbcontext.start()
        yield dbcontext
    finally:
        dbcontext.finish()
