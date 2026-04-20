from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.future import select 
from sqlalchemy.ext.asyncio import AsyncSession 
from .. import models,schemas,utils,database,oauth2

router = APIRouter(
    tags = ['Auth']
)

@router.post('/login', response_model = schemas.Token)
async def user_login(user_credentials : OAuth2PasswordRequestForm = Depends() , db : AsyncSession = Depends(database.get_db)):

    result = await db.execute(
        select(models.User)
        .where(models.User.email == user_credentials.username)
    )
    user = result.scalar_one_or_none() 

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Invalid User Credentials')

    if not utils.verify_login(user_credentials.password,user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Invalid User Credentials')

    access_token = await oauth2.create_access_token(data = {"user_id": user.id})

    return { "access_token" : access_token, "token_type":"bearer"}
