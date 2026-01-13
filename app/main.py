from asyncio import run
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine
from app.models.base_model import BaseModel
from app.routes import auth_route, healthmonitor_route


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_models()

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    run(init_models())


app.include_router(auth_route.router)
app.include_router(healthmonitor_route.router)
