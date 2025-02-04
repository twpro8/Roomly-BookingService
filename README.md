
docker create network momoa-network

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=booking \
    --network=momoa-network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_redis \
    -p 7379:6379 \
    --network=momoa-network \
    -d redis:7

docker run --name booking_backend \
    -p 7878:8000 \
    --network=momoa-network \
    booking_image

docker run --name booking_celery_worker \
    --network=momoa-network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
    --network=momoa-network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker build -t booking_image .
