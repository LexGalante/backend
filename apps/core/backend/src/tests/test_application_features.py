import pytest
from fastapi import status

from tests.helpers import prepare_headers, clean_feature


def setup_module(module):
    clean_feature(["test1", "test2", "test3", "test4", "test5", "test6"])


def test_get_should_return_features(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications/netflix/features", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json) >= 1


def test_get_should_not_return_features_because_missing_token(http_client, jwt_token):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications/netflix/features", headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_create_new_feature(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    new_feature = {
        "environment_id": 4,
        "name": feature_name,
        "enable": True,
    }
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/",
        headers=prepare_headers(jwt_token),
        json=new_feature)
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(initial_features) != len(json)


def test_patch_should_not_create_new_feature_because_missing_token(http_client, jwt_token):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    new_feature = {
        "environment_id": 4,
        "name": "test",
        "enable": True,
    }
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/",
        headers=prepare_headers(),
        json=new_feature)
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


def test_patch_should_not_create_new_feature_because_feature_already_exists(http_client, jwt_token):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    new_feature = {
        "environment_id": 4,
        "name": "test1",
        "enable": True,
    }
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/",
        headers=prepare_headers(jwt_token),
        json=new_feature)
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "The feature(test1) already exists this environment" in json["errors"]


@pytest.mark.parametrize("feature_name", ["test4", "test5", "test6"])
def test_patch_should_create_new_feature_in_all_environment(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    new_feature = {
        "environment_id": 0,
        "name": feature_name,
        "enable": True,
        "all": True
    }
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/",
        headers=prepare_headers(jwt_token),
        json=new_feature)
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(initial_features) != len(json)


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_activate_feature_in_environment(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/{feature_name}/1/activate",
        headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    for feature in json:
        if feature["name"] == feature_name and feature["environment_id"] == 1:
            assert feature["enable"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_not_activate_feature_in_environment_because_missing_token(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/{feature_name}/1/activate",
        headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_activate_all_feature_in_all_environment(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/activate-all",
        headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    for feature in json:
        assert feature["enable"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_not_activate_all_feature_in_all_environment_because_missing_token(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/activate-all",
        headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_inactivate_feature_in_environment(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/{feature_name}/1/inactivate",
        headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    for feature in json:
        if feature["name"] == feature_name and feature["environment_id"] == 1:
            assert not feature["enable"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_not_inactivate_feature_in_environment_because_missing_token(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/{feature_name}/1/inactivate",
        headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_inactivate_all_feature_in_all_environment(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/inactivate-all",
        headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    for feature in json:
        assert not feature["enable"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_patch_should_not_inactivate_all_feature_in_all_environment_because_missing_token(http_client, jwt_token, feature_name):
    # ARRANGE
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.patch(
        "/v1/applications/netflix/features/inactivate-all",
        headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_delete_should_feature_application(http_client, jwt_token, feature_name):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.delete(f"/v1/applications/netflix/features/{feature_name}", headers=prepare_headers(jwt_token))
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(initial_features) != len(json)


@pytest.mark.parametrize("feature_name", ["test1", "test2", "test3"])
def test_delete_should_not_feature_application_because_missing_token(http_client, jwt_token, feature_name):
    # ARRANGE & ACT
    response = http_client.get("/v1/applications/netflix/features/", headers=prepare_headers(jwt_token))
    assert response.status_code == status.HTTP_200_OK
    initial_features = response.json()
    assert len(initial_features) > 0
    # ACT
    response = http_client.delete(f"/v1/applications/netflix/features/{feature_name}", headers=prepare_headers())
    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert "Not authenticated" in json["errors"]


def teardown_module(module):
    clean_feature(["test1", "test2", "test3", "test4", "test5", "test6"])
