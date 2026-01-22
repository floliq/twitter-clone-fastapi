import io

import pytest


@pytest.mark.anyio
async def test_upload_media_by_unauthorized(client):
    file_content = b"fake image content"
    file_like = io.BytesIO(file_content)
    files = {"file": ("test_image.jpg", file_like, "image/jpeg")}

    response = await client.post("/api/medias", files=files)
    assert response.status_code == 401
    assert response.json() == {"detail": "API key is required"}


@pytest.mark.anyio
async def test_upload_media_by_authorized(auth_client):
    file_content = b"fake image content"
    file_like = io.BytesIO(file_content)
    files = {"file": ("test_image.jpg", file_like, "image/jpeg")}

    response = await auth_client.post("/api/medias", files=files)
    assert response.status_code == 200
    assert response.json() == {"result": True, "media_id": 1}


@pytest.mark.anyio
async def test_upload_media_empty_content(auth_client):
    file_content = b""
    file_like = io.BytesIO(file_content)
    files = {"file": ("test_image.jpg", file_like, "image/jpeg")}

    response = await auth_client.post("/api/medias", files=files)
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot to upload empty file"}


@pytest.mark.anyio
async def test_upload_media_invalid_format(auth_client):
    file_content = b"fake image content"
    file_like = io.BytesIO(file_content)
    files = {"file": ("test_image.pdf", file_like, "application/pdf")}

    response = await auth_client.post("/api/medias", files=files)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid picture file format"}
