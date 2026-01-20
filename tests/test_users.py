import pytest


@pytest.mark.anyio
async def test_get_me_by_unauthorized(client):
    response = await client.get("/api/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "No authorization"}


@pytest.mark.anyio
async def test_get_me_by_authorized(auth_client, sample_user):
    response = await auth_client.get("/api/users/me")
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "user": {"id": sample_user.id, "name": sample_user.username, "followers": [], "following": []},
    }
