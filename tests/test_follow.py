import pytest


@pytest.mark.anyio
async def test_follow_by_unauthorized(client, another_user):
    response = await client.post(f"/api/users/{another_user.id}/follow")

    assert response.status_code == 401
    assert response.json() == {"result": False, "error_type": "auth_error", "error_message": "API key is required"}


@pytest.mark.anyio
async def test_follow_by_authorized(auth_client, another_user):
    response = await auth_client.post(f"/api/users/{another_user.id}/follow")

    assert response.status_code == 200
    assert response.json() == {"result": True}


@pytest.mark.anyio
async def test_follow_to_yourself_by_authorized(auth_client, sample_user):
    response = await auth_client.post(f"/api/users/{sample_user.id}/follow")

    assert response.status_code == 400
    assert response.json() == {
        "result": False,
        "error_type": "validation_error",
        "error_message": "Can't follow to yourself",
    }


@pytest.mark.anyio
async def test_exists_follow_by_authorized(auth_client, another_user, sample_follow_by_sample_user):
    response = await auth_client.post(f"/api/users/{another_user.id}/follow")

    assert response.status_code == 400
    assert response.json() == {
        "result": False,
        "error_type": "validation_error",
        "error_message": "Follow is already exists",
    }


@pytest.mark.anyio
async def test_unfollow_by_unauthorized(client, another_user, sample_follow_by_sample_user):
    response = await client.delete(f"/api/users/{another_user.id}/follow")

    assert response.status_code == 401
    assert response.json() == {"result": False, "error_type": "auth_error", "error_message": "API key is required"}


@pytest.mark.anyio
async def test_unexists_follow_by_authorized(auth_client, another_user):
    response = await auth_client.delete(f"/api/users/{another_user.id}/follow")

    assert response.status_code == 404
    assert response.json() == {"result": False, "error_type": "validation_error", "error_message": "Follow not found"}


@pytest.mark.anyio
async def test_unfollow_to_yourself_by_authorized(auth_client, sample_user):
    response = await auth_client.delete(f"/api/users/{sample_user.id}/follow")

    assert response.status_code == 400
    assert response.json() == {
        "result": False,
        "error_type": "validation_error",
        "error_message": "Can't unfollow to yourself",
    }


@pytest.mark.anyio
async def test_unfollow_by_authorized(auth_client, another_user, sample_follow_by_sample_user):
    response = await auth_client.delete(f"/api/users/{another_user.id}/follow")

    assert response.status_code == 200
    assert response.json() == {"result": True}
