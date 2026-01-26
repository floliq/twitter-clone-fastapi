from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.depends import CurrentUser, MediaServiceAnnotation

media_router = APIRouter(prefix="/api/medias")

ALLOWED_MIME = ("image/jpeg", "image/png", "image/webp", "video/mp4", "image/x-icon")


@media_router.post("")
async def upload_medias(
    current_user: CurrentUser, media_service: MediaServiceAnnotation, file: Annotated[UploadFile, File(...)]
):
    if file.content_type and file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid picture file format")

    return await media_service.upload_file(file)
