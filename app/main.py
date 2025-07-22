from fastapi import FastAPI
from models import Base
from database import engine
from routes import router as api_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router)
