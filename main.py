import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI,APIRouter
from app import models
from app.database import engine, AsyncSessionLocal, Base
from app.routers import users,expenses,auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings

#hi


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run table creation on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(auth.router)





@app.get("/")
async def home():
    return FileResponse("app/static/login.html")

app.mount("/", StaticFiles(directory="app/static"), name="static")
