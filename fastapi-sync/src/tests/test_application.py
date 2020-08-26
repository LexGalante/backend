import pytest
from fastapi import status

from tests.helpers import prepare_headers, execute_sql, get_bigger_text


def test_get_should_return_applications_of_user_logged(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json) >= 3


def test_get_should_not_return_applications_because_missing_token(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications", headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("application", ["netflix", "whats_app"])
def test_get_by_name_should_return_applications_of_user_logged(http_client, jwt_token, application):
    # ARRANGE & ACT
    response = http_client.get(f"/v1/applications/{application}", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "name" in json.keys()
    assert json["name"] == application

@pytest.mark.parametrize("application", ["netflix", "whats_app"])
def test_get_by_name_should_not_return_applications_because_missing_token(http_client, jwt_token, application):
    # ARRANGE & ACT
    response = http_client.get(f"/v1/applications/{application}", headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("application", ["netflixxx", "whats_appppp"])
def test_get_by_name_should_not_return_applications_because_application_not_exists(http_client, jwt_token, application):
    # ARRANGE & ACT
    response = http_client.get(f"/v1/applications/{application}", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert f"Not found or Not permission access application {application}" in json["errors"]


def test_post_should_execute_success(http_client, jwt_token):
    # ARRANGE & ACT
    application = {
        "real_name": "Slack",
        "model": 3,
        "description": "Sending and receive videos, messages, gifs, documents...",
        "details": "https://slack.com.br"
    }
    response = http_client.post("/v1/applications/", headers=prepare_headers(jwt_token), json=application)
    # ASSERT
    assert response.status_code == status.HTTP_201_CREATED
    json = response.json()
    assert "name" in json.keys()
    assert json["name"] == "slack"


def test_post_should_not_execute_because_missing_token(http_client):
    # ARRANGE & ACT
    application = {
        "real_name": "Office365",
        "model": 3,
        "description": "Microsoft utilities",
        "details": "https://office365.com"
    }
    response = http_client.post("/v1/applications/", headers=prepare_headers(), json=application)
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


def test_post_should_not_execute_because_missing_field_real_name(http_client, jwt_token):
    # ARRANGE & ACT
    application = {
        "model": 3,
        "description": "Sending and receive videos, messages, gifs, documents...",
        "details": "https://slack.com.br"
    }
    response = http_client.post("/v1/applications/", headers=prepare_headers(jwt_token), json=application)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("real_name", ["1", "2", get_bigger_text()])
def test_post_should_not_execute_because_field_real_name_is_invalid(http_client, jwt_token, real_name):
    # ARRANGE & ACT
    application = {
        "real_name": real_name,
        "model": 3,
        "description": get_bigger_text(),
        "details": "https://slack.com.br"
    }
    response = http_client.post("/v1/applications/", headers=prepare_headers(jwt_token), json=application)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_post_should_not_execute_because_missing_field_model(http_client, jwt_token):
    # ARRANGE & ACT
    application = {
        "real_name": "Python",
        "description": "SDK for python 3",
        "details": "https://python.org"
    }
    response = http_client.post("/v1/applications/", headers=prepare_headers(jwt_token), json=application)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("model", [0, 4, 5, 6, 99])
def test_post_should_not_execute_because_field_model_is_invalid(http_client, jwt_token, model):
    # ARRANGE & ACT
    application = {
        "real_name": "Python",
        "model": model,
        "description": "SDK for python 3",
        "details": "https://python.org"
    }
    response = http_client.post("/v1/applications/", headers=prepare_headers(jwt_token), json=application)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_post_should_not_execute_because_missing_field_description(http_client, jwt_token):
    # ARRANGE & ACT
    application = {
        "real_name": "Python",
        "model": 3,
        "details": "https://python.org"
    }
    response = http_client.post("/v1/applications/", headers=prepare_headers(jwt_token), json=application)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("description", ["", "23456789", get_bigger_text()])
def test_post_should_not_execute_because_field_description_is_invalid(http_client, jwt_token, description):
    # ARRANGE & ACT
    application = {
        "real_name": "Python",
        "model": 3,
        "description": description,
        "details": "https://python.org"
    }
    response = http_client.post("/v1/applications/", headers=prepare_headers(jwt_token), json=application)
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def teardown_module(module):
    execute_sql("DELETE FROM application_users WHERE application_id = (SELECT MAX(id) FROM applications)", {})
    execute_sql("DELETE FROM applications WHERE name = :name", {"name": "slack"})
