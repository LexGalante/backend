import pytest
from fastapi import status

from tests.helpers import execute_clean_data


def setup_module(module):
    execute_clean_data("DELETE FROM users WHERE email = :email", {"email": "fulano@iggle.com"})


def test_register_should_execute_with_success(http_client):
    # ARRANGE
    user = {"email": "fulano@iggle.com", "password": "Minh@SenhaSegura123"}
    # ACT
    response = http_client.post("/v1/register/", json=user)
    # ASSERT
    assert response.status_code == status.HTTP_201_CREATED
    json = response.json()
    assert "id" in json.keys()
    assert json["id"] > 0


def test_register_should_not_execute_without_email(http_client):
    # ARRANGE
    user = {"email": "fulano@iggle.com"}
    # ACT
    response = http_client.post("/v1/register/", json=user)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_should_not_execute_without_password(http_client):
    # ARRANGE
    user = {"password": "Minh@SenhaSegura123"}
    # ACT
    response = http_client.post("/v1/register/", json=user)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("password", ["123", "1234", "aaa123", "1111qaaa"])
def test_register_should_not_execute_with_weak_password(http_client, password):
    # ARRANGE
    user = {"email": "fulano@iggle.com", "password": "123"}
    # ACT
    response = http_client.post("/v1/register/", json=user)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def teardown_module(module):
    execute_clean_data("DELETE FROM users WHERE email = :email", {"email": "fulano@iggle.com"})
