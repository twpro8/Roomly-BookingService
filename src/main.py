import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI

from src.api.auth import router as auth_router
from src.api.hotels import router as hotels_router

app = FastAPI(title="Momoa Web API")
app.include_router(auth_router)
app.include_router(hotels_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True) # you can add workers but reload must be false