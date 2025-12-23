from asyncio import run
from fastapi import FastAPI
from app.models.base_model import BaseModel
from app.core.database import engine

app = FastAPI()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

if __name__ == "__main__":
    run(init_models())


@app.get("/")
async def read_root():
    return {"Hello": "World"}
