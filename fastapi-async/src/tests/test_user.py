import pytest
from fastapi import status

from tests.helpers import generate_users, clean_users, prepare_headers


def setup_module(module):
    generate_users(10)


def test_get_should_return_correct_paginate_users(http_client, jwt_token):
    # ARRANGE & ACT
    response_page_1 = http_client.get(
        "/v1/users/paginate/1/5",
        headers=prepare_headers(jwt_token))
    response_page_2 = http_client.get(
        "/v1/users/paginate/1/10",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt_token}"
        })
    # ASSERT
    assert response_page_1.status_code == status.HTTP_200_OK
    assert response_page_2.status_code == status.HTTP_200_OK
    json_1 = response_page_1.json()
    json_2 = response_page_2.json()
    assert len(json_1) == 5
    assert len(json_2) == 10


def test_get_should_not_paginate_users_because_missing_token(http_client):
    # ARRANGE & ACT
    response = http_client.get("/v1/users/paginate/1/10", headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("email", ["alex@iggle.com", "amanda@iggle.com"])
def test_get_by_email_should_return_user(http_client, jwt_token, email):
    # ARRANGE & ACT
    response = http_client.get(
        f"/v1/users/{email}",
        headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "email" in json.keys()
    assert json["email"] == email


@pytest.mark.parametrize("email", ["alex@iggle.com"])
def test_get_by_email_should_not_return_user_because_missing_token(http_client, jwt_token, email):
    # ARRANGE & ACT
    response = http_client.get(f"/v1/users/{email}", headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("email", ["aaa@iggle.com"])
def test_get_by_email_should_not_return_user_because_doesnt_exists(http_client, jwt_token, email):
    # ARRANGE & ACT
    response = http_client.get(f"/v1/users/{email}", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "errors" in json.keys()
    assert f"{email} doesn't exists" in json["errors"]


def teardown_module(module):
    clean_users(10)
