from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select 
from sqlalchemy.ext.asyncio import AsyncSession 
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

async def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

async def verify_access_token(token : str , credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])

        id = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception

    return token_data

async def get_current_user(token : str = Depends(oauth2_scheme), db : AsyncSession = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = f"Could not validate Credentials", headers = {"WWW-Authenticate" : "Bearer"})

    token_data = await verify_access_token(token , credentials_exception)

    result = await db.execute(
        select(models.User).where(models.User.id == token_data.id)
    )
    user = result.scalar_one_or_none() 

    return user

