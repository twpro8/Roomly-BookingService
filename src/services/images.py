import shutil

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    def upload_image(self, file):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)
            resize_image.delay(image_path)
