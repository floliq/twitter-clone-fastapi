from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.depends import CurrentUser, MediaServiceAnnotation
from app.schemas.media import Media

media_router = APIRouter(prefix="/api/medias")

ALLOWED_MIME = ("image/jpeg", "image/png", "image/webp", "video/mp4", "image/x-icon")


@media_router.post(
    "",
    summary="Upload media file",
    description=(
        "Upload a media file (image or video) for the current user. "
        "Allowed MIME types: image/jpeg, image/png, image/webp, video/mp4, image/x-icon."
    ),
    response_description="Uploaded file metadata with media_id",
    response_model=Media,
    responses={
        400: {
            "description": "Bad Request. File format not allowed, empty filename or file, etc.",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_format": {
                            "summary": "Invalid file format",
                            "value": {"detail": "Invalid picture file format"},
                        },
                        "empty_filename": {
                            "summary": "Empty filename",
                            "value": {"detail": "Filename cannot be empty"},
                        },
                        "empty_file": {
                            "summary": "Empty file",
                            "value": {"detail": "Cannot to upload empty file"},
                        },
                    }
                }
            },
        }
    },
)
async def upload_medias(
    current_user: CurrentUser,
    media_service: MediaServiceAnnotation,
    file: Annotated[
        UploadFile, File(..., description="Media file to upload. Allowed types: jpeg, png, webp, mp4, x-icon.")
    ],
):
    if file.content_type and file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid picture file format")

    return await media_service.upload_file(file)
