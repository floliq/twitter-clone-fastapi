import pytest


@pytest.mark.anyio
async def test_get_tweets_by_unauthorized(client):
    response = await client.get("/api/tweets")
    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required"}


@pytest.mark.anyio
async def test_get_tweets_by_authorized(
    auth_client,
    sample_user,
    sample_tweet,
    another_tweet,
    sample_attachment,
    another_attachment,
    sample_like_by_sample_user,
    sample_like_by_another_user,
    sample_like_to_another_user_tweet,
    sample_tweet_by_another_user,
    sample_follow_by_sample_user,
    another_user,
):
    response = await auth_client.get("/api/tweets")
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "tweets": [
            {
                "id": sample_tweet.id,
                "content": sample_tweet.content,
                "author": {"id": sample_user.id, "name": sample_user.username},
                "attachments": [sample_attachment.path, another_attachment.path],
                "likes": [
                    {"user_id": sample_user.id, "name": sample_user.username},
                    {"user_id": another_user.id, "name": another_user.username},
                ],
            },
            {
                "id": sample_tweet_by_another_user.id,
                "content": sample_tweet_by_another_user.content,
                "author": {"id": another_user.id, "name": another_user.username},
                "attachments": [],
                "likes": [
                    {"user_id": sample_user.id, "name": sample_user.username},
                ],
            },
            {
                "id": another_tweet.id,
                "content": another_tweet.content,
                "author": {"id": sample_user.id, "name": sample_user.username},
                "attachments": [],
                "likes": [],
            },
        ],
    }


@pytest.mark.anyio
async def test_create_tweet_by_unauthorized(client):
    response = await client.post("/api/tweets", json={"tweet_data": "New tweet"})

    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required"}


@pytest.mark.anyio
async def test_create_tweet_by_authorized(auth_client, attachment_without_tweet):
    response = await auth_client.post(
        "/api/tweets", json={"tweet_data": "New tweet", "tweet_media_ids": [attachment_without_tweet.id]}
    )

    assert response.status_code == 201
    assert response.json() == {"result": True, "tweet_id": 1}


@pytest.mark.anyio
async def test_delete_tweet_by_unauthorized(client, sample_tweet):
    response = await client.delete(f"/api/tweets/{sample_tweet.id}")

    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required"}


@pytest.mark.anyio
async def test_delete_unexist_tweet(auth_client):
    response = await auth_client.delete("/api/tweets/15")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tweet not found"}


@pytest.mark.anyio
async def test_delete_tweet_by_authorized(auth_client, sample_tweet):
    response = await auth_client.delete(f"/api/tweets/{sample_tweet.id}")

    assert response.status_code == 200
    assert response.json() == {"result": True}
