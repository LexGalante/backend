import pytest
from fastapi import status

from tests.helpers import prepare_headers, generate_application, execute_sql


def setup_module(module):
    generate_application("botica")


def test_get_should_return_success(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications/netflix/users", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json) >= 1


def test_get_should_not_return_because_missing_token(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications/netflix/users", headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


def test_get_should_not_return_because_user_doesnt_have_permission(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications/botica/users", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == []


def test_patch_should_create_user_in_application(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.patch(
        "/v1/applications/netflix/users/",
        headers=prepare_headers(jwt_token),
        json={"user_id": 3})
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json) > 1


def test_patch_should_not_create_user_because_missing_token(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.patch(
        "/v1/applications/netflix/users/",
        headers=prepare_headers(),
        json={"user_id": 3})
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


def test_patch_should_not_create_user_because_field_is_invalid(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.patch(
        "/v1/applications/netflix/users/",
        headers=prepare_headers(jwt_token),
        json={"x": "x"})
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_patch_should_not_create_user_because_user_not_exists(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.patch(
        "/v1/applications/netflix/users/",
        headers=prepare_headers(jwt_token),
        json={"user_id": 999999999})
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "The user(999999999) cannot possible to add in application netflix" in json["errors"]


def test_remove_should_remove_user(http_client, jwt_token):
    # ARRANGE
    response = http_client.patch(
        "/v1/applications/netflix/users/",
        headers=prepare_headers(),
        json={"user_id": 3})
    assert response.status_code == status.HTTP_200_OK
    response = http_client.get("/v1/applications/netflix/users", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    # ACT
    response = http_client.delete("/v1/applications/netflix/users/3", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(users) != len(json)


def test_remove_should_not_remove_because_user_doesnt_have_permission(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.delete("/v1/applications/botica/users/3", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == []


def teardown_module(module):
    execute_sql("DELETE FROM application_users WHERE user_id = :user_id", {"user_id": 3})
    execute_sql("DELETE FROM applications WHERE name = :name", {"name": "slack"})
