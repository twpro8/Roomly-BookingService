import asyncio
import logging
import os

from PIL import Image

from src.database import null_pool_session_maker
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def resize_image(image_path: str):
    logging.debug("The image_path function is called")
    sizes = [500, 200]
    output_folder = "src/static/images"
    img = Image.open(image_path)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )
        new_file_name = f"{name}_{size}px{ext}"
        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)

    logging.info(
        f"The image is saved in the following sizes: {sizes} in the folder {output_folder}"
    )


async def get_checkin_days_helper():
    logging.debug("The get_checkin_days_helper function is called")
    async with DBManager(session_factory=null_pool_session_maker) as db:
        bookings = await db.bookings.get_checkin_day()
        logging.info(f"Bookings={bookings}")


@celery_instance.task(name="checkin_day")
def send_emails_when_checkin():
    logging.debug("The send_emails_when_checkin function is called")
    asyncio.run(get_checkin_days_helper())
