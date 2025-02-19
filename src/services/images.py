from src.exceptions import UnsupportedImageFormatException, ImageTooLargeException
from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    @staticmethod
    def upload_image(file):
        allowed_extensions = ["image/jpeg", "image/png"]
        if file.content_type not in allowed_extensions:
            raise UnsupportedImageFormatException

        max_file_size = 5242880  # 5 MB
        file_content = file.file.read()
        if len(file_content) > max_file_size:
            raise ImageTooLargeException

        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            new_file.write(file_content)
            resize_image.delay(image_path)
