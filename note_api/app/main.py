from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import create_table
from .routers import router



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield# 缺少这行导入


app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

