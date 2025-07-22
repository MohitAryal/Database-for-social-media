from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routes import router as api_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router)
