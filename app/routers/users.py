from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from app.database import get_db
from app import models,schemas,utils
from sqlalchemy.orm import sessionmaker,Session

router = APIRouter(
       prefix = "/users",
       tags = ['Users'] #Just organises the documentation
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.UserResponse )
async def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
     #hashing the password - user.password
     hashed_password = utils.hash(user.password)
     user.password = hashed_password
     new_user = models.User(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user

@router.get("/{id}", response_model = schemas.UserResponse)
async def get_user(id : int, db : Session = Depends(get_db)):
          user = db.query(models.User).filter(models.User.id == id).first()
          if not user:
               raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with {id} : id not found")
          return user