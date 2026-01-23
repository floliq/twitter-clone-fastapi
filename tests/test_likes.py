import pytest


@pytest.mark.anyio
async def test_like_tweet_by_unauthorized(client, sample_tweet):
    response = await client.post(f"/api/tweets/{sample_tweet.id}/likes")

    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required"}


@pytest.mark.anyio
async def test_like_tweet_by_authorized(auth_client, sample_tweet):
    response = await auth_client.post(f"/api/tweets/{sample_tweet.id}/likes")

    assert response.status_code == 200
    assert response.json() == {"result": True}


@pytest.mark.anyio
async def test_exists_like_tweet_by_authorized(auth_client, sample_tweet, sample_like_by_sample_user):
    response = await auth_client.post(f"/api/tweets/{sample_tweet.id}/likes")

    assert response.status_code == 400
    assert response.json() == {"detail": "Like is already exists"}


@pytest.mark.anyio
async def test_remove_like_tweet_by_unauthorized(client, sample_tweet, sample_user, sample_like_by_sample_user):
    response = await client.delete(f"/api/tweets/{sample_tweet.id}/likes")

    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required"}


@pytest.mark.anyio
async def test_remove_unexists_like_tweet_by_authorized(auth_client, sample_tweet):
    response = await auth_client.delete(f"/api/tweets/{sample_tweet.id}/likes")

    assert response.status_code == 404
    assert response.json() == {"detail": "Like not found"}


@pytest.mark.anyio
async def test_remove_like_tweet_by_authorized(auth_client, sample_tweet, sample_user, sample_like_by_sample_user):
    response = await auth_client.delete(f"/api/tweets/{sample_tweet.id}/likes")

    assert response.status_code == 200
    assert response.json() == {"result": True}
