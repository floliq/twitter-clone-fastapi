import pytest


@pytest.mark.anyio
async def test_get_me_by_unauthorized(client):
    response = await client.get("/api/users/me")
    assert response.status_code == 401
    assert response.json() == {"result": False, "error_type": "auth_error", "error_message": "API key is required"}


@pytest.mark.anyio
async def test_get_me_by_wrong_api_key_client(wrong_api_key_client):
    response = await wrong_api_key_client.get("/api/users/me")
    assert response.status_code == 401
    assert response.json() == {"result": False, "error_type": "auth_error", "error_message": "User not found"}


@pytest.mark.anyio
async def test_get_me_by_authorized(
    auth_client, sample_user, another_user, sample_follow_by_sample_user, sample_follow_by_another_user
):
    response = await auth_client.get("/api/users/me")
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "user": {
            "id": sample_user.id,
            "name": sample_user.username,
            "followers": [{"id": another_user.id, "name": another_user.username}],
            "following": [{"id": another_user.id, "name": another_user.username}],
        },
    }


@pytest.mark.anyio
async def test_get_user_by_unauthorized(client, sample_user):
    response = await client.get(f"/api/users/{sample_user.id}")
    assert response.status_code == 401
    assert response.json() == {"result": False, "error_type": "auth_error", "error_message": "API key is required"}


@pytest.mark.anyio
async def test_get_user_by_authorized(
    auth_client, another_user, sample_user, sample_follow_by_sample_user, sample_follow_by_another_user
):
    response = await auth_client.get(f"/api/users/{another_user.id}")
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "user": {
            "id": another_user.id,
            "name": another_user.username,
            "followers": [{"id": sample_user.id, "name": sample_user.username}],
            "following": [{"id": sample_user.id, "name": sample_user.username}],
        },
    }
