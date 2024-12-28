from fastapi import FastAPI
from hotels import router as hotels_router


app = FastAPI(title="Momoa Web API",)
app.include_router(hotels_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True) # you can add workers but reload must be false