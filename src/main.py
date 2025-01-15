import sys
from contextlib import asynccontextmanager
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI

from src import redis_manager
from src.api.auth import router as auth_router
from src.api.hotels import router as hotels_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.close()


app = FastAPI(title="Momoa Web API", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True) # you can add workers but reload must be false