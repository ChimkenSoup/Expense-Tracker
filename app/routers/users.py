from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
# CHANGED: Removed synchronous Session import, now using AsyncSession
# from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.future import select  # NEW: SQLAlchemy 2.0 async style queries
from sqlalchemy.ext.asyncio import AsyncSession  # NEW: Async session for non-blocking DB calls
from app.database import get_db
from app import models,schemas,utils

router = APIRouter(
       prefix = "/users",
       tags = ['Users'] #Just organises the documentation
)

# CHANGED: db parameter type from Session to AsyncSession
@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.UserResponse )
async def create_user(user : schemas.UserCreate, db : AsyncSession = Depends(get_db)):
     #hashing the password - user.password
     hashed_password = utils.hash(user.password)
     user.password = hashed_password
     new_user = models.User(**user.dict())
     db.add(new_user)
     # CHANGED: db.commit() and db.refresh() are now awaited because they're async operations
     await db.commit()  # ASYNC: must await because it writes to DB
     await db.refresh(new_user)  # ASYNC: must await to refresh the object with DB values
     return new_user
     # OLD: db.commit() and db.refresh() were synchronous and blocked the thread

# CHANGED: db parameter type from Session to AsyncSession
@router.get("/{id}", response_model = schemas.UserResponse)
async def get_user(id : int, db : AsyncSession = Depends(get_db)):
    # CHANGED: Using await db.execute(select().where()) instead of db.query().filter().first()
    # This is async and won't block other requests while waiting for DB response
    result = await db.execute(
        select(models.User)
        .where(models.User.id == id)
    )
    user = result.scalar_one_or_none()  # NEW: scalar_one_or_none() gets first result or None
    # OLD: user = db.query(models.User).filter(models.User.id == id).first()
    # OLD: This blocked the entire worker thread while waiting for DB

    if not user:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with {id} : id not found")
    return user
