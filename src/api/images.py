from fastapi import APIRouter, UploadFile

from src.exceptions import (
    ImageTooLargeException,
    ImageTooLargeHTTPException,
    UnsupportedImageFormatException,
    UnsupportedImageFormatHTTPException,
)
from src.services.images import ImageService

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("")
def upload_image(file: UploadFile):
    try:
        ImageService().upload_image(file)
    except ImageTooLargeException:
        raise ImageTooLargeHTTPException
    except UnsupportedImageFormatException:
        raise UnsupportedImageFormatHTTPException
    return {"status": "ok"}
