import pytest
from fastapi import status


@pytest.mark.parametrize("username", ["alex", "amanda", "nino", "bibi"])
def test_login_should_success_when_username_and_password_is_correct(http_client, username):
    # ARRANGE
    user = {"username": f"{username}@iggle.com", "password": "Minh@SenhaSegura123"}
    # ACT
    response = http_client.post("/v1/login/", json=user)
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "token_type" in json.keys()
    assert "access_token" in json.keys()


def test_login_should_fails_when_username_and_password_is_correct(http_client):
    # ARRANGE
    user = {"username": "xpto@iggle.com", "password": "Minh@SenhaSegura123"}
    # ACT
    response = http_client.post("/v1/login/", json=user)
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "errors" in json.keys()


def test_login_should_fails_when_username_is_null(http_client):
    # ARRANGE
    user = {"password": "Minh@SenhaSegura123"}
    # ACT
    response = http_client.post("/v1/login/", json=user)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_should_fails_when_password_is_null(http_client):
    # ARRANGE
    user = {"username": "xpto@iggle.com"}
    # ACT
    response = http_client.post("/v1/login/", json=user)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

