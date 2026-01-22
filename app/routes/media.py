from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.depends import get_current_user, get_media_service
from app.services.media import MediaService

media_router = APIRouter(prefix="/api/medias")

ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "video/mp4", "image/x-icon"}


@media_router.post("")
async def upload_medias(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    media_service: MediaService = Depends(get_media_service),
):
    if file.content_type and file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid picture file format")

    return await media_service.upload_file(file)
