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

    async def upload_file(self, upload_file: UploadFile):
        if not upload_file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename cannot be empty")

        upload_name = self._generate_upload_name(upload_file.filename)
        path_to = MEDIA_DIR / upload_name

        async with aiofiles.open(path_to, "wb") as buffer:
            await buffer.write(await upload_file.read())

        if path_to.stat().st_size == 0:
            path_to.unlink(missing_ok=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot to upload empty file")

        uploaded_file = await self.repository.upload_file(f"media/{upload_name}")
        return Media(result=True, media_id=uploaded_file.id)

    def _generate_upload_name(self, filename: str) -> str:
        file_uuid = uuid.uuid4().hex
        file_extension = Path(filename).suffix
        return f"{file_uuid}{file_extension}"
