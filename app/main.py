from asyncio import run
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.core.config import UI
from app.core.database import engine
from app.models.base_model import BaseModel
from app.routes import auth_route, healthmonitor_route
from app.services.auth_service import AuthService


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_models()

    yield

    await engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    dependencies=[Depends(AuthService.validate_tg_hash)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[UI],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HTTPSRedirectMiddleware)

if __name__ == "__main__":
    run(init_models())


app.include_router(auth_route.router)
app.include_router(healthmonitor_route.router)
