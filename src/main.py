from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.db.database import engine, Base
from contextlib import asynccontextmanager
from src.routes import quiz


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])

# Healthcheck API endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "OK", "message": "Service is running."},
        status_code=200,
    )

