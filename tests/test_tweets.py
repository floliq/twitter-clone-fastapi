import pytest


@pytest.mark.anyio
async def test_get_tweets_by_unauthorized(client):
    response = await client.get("/api/tweets")
    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required"}


@pytest.mark.anyio
async def test_get_tweets_by_authorized(
    auth_client, sample_user, sample_tweet, another_tweet, sample_attachment, another_attachment
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
                "likes": [],
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

    assert response.status_code == 200
    assert response.json() == {"result": True, "tweet_id": 1}
