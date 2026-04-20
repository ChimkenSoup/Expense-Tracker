from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.params import Body

from sqlalchemy.future import select 
from sqlalchemy.ext.asyncio import AsyncSession 
from app.database import get_db
from app import models,schemas,utils

router = APIRouter(
       prefix = "/users",
       tags = ['Users']
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.UserResponse )
async def create_user(user : schemas.UserCreate, db : AsyncSession = Depends(get_db)):

     hashed_password = utils.hash(user.password)
     user.password = hashed_password
     new_user = models.User(**user.dict())
     db.add(new_user)

     await db.commit() 
     await db.refresh(new_user) 
     return new_user

@router.get("/{id}", response_model = schemas.UserResponse)
async def get_user(id : int, db : AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(models.User)
        .where(models.User.id == id)
    )
    user = result.scalar_one_or_none() 

    if not user:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with {id} : id not found")
    return user
