from fastapi import FastAPI,APIRouter
from app import models
from app.database import engine
from app.routers import users,expenses,auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()

app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(auth.router)


models.Base.metadata.create_all(bind = engine)


@app.get("/")
async def home():
    return FileResponse("app/static/login.html")

app.mount("/", StaticFiles(directory="app/static"), name="static")



 