import uuid
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile, status

from app.repositories.media import MediaRepository
from app.schemas.media import Media

MEDIA_DIR = Path("app/media")
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


class MediaService:
    def __init__(self, repository: MediaRepository):
        self.repository = repository

    async def upload_file(self, file: UploadFile):
        filename = file.filename
        if not filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename cannot be empty")

        extension = Path(filename).suffix

        upload_name = f"{uuid.uuid4().hex}{extension}"

        path_to = MEDIA_DIR / upload_name

        async with aiofiles.open(path_to, "wb") as buffer:
            data = await file.read()
            await buffer.write(data)

        if path_to.stat().st_size == 0:
            try:
                path_to.unlink(missing_ok=True)
            finally:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot to upload empty file")

        uploaded_file = await self.repository.upload_file(f"media/{upload_name}")

        return Media(result=True, media_id=uploaded_file.id)
