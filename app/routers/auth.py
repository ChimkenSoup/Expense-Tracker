from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# CHANGED: Removed synchronous Session import, now using AsyncSession
# from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.future import select  # NEW: SQLAlchemy 2.0 async style queries
from sqlalchemy.ext.asyncio import AsyncSession  # NEW: Async session for non-blocking DB calls
from .. import models,schemas,utils,database,oauth2

router = APIRouter(
    tags = ['Auth']
)

# CHANGED: db parameter type from Session to AsyncSession
@router.post('/login', response_model = schemas.Token)
async def user_login(user_credentials : OAuth2PasswordRequestForm = Depends() , db : AsyncSession = Depends(database.get_db)):
    #oauth2form has username and password as fields
    #{
       # "username":"example@gmail.com",
        #"password":"nice"
    #}
    #abpce is example

    # CHANGED: Using await db.execute(select().where()) instead of db.query().filter().first()
    # This is async and won't block other requests while waiting for DB response
    result = await db.execute(
        select(models.User)
        .where(models.User.email == user_credentials.username)
    )
    user = result.scalar_one_or_none()  # Gets first result or None
    # OLD: user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # OLD: This blocked the entire worker thread while waiting for DB

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Invalid User Credentials')

    if not utils.verify_login(user_credentials.password,user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Invalid User Credentials')

    access_token = await oauth2.create_access_token(data = {"user_id": user.id})

    return { "access_token" : access_token, "token_type":"bearer"}
