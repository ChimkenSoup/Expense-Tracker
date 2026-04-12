from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
# CHANGED: Removed synchronous Session import, now using AsyncSession
# from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.future import select  # NEW: SQLAlchemy 2.0 async style queries
from sqlalchemy.ext.asyncio import AsyncSession  # NEW: Async session for non-blocking DB calls
from app.config import settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')
#TElls the api about the login endpoint
#oauth2_scheme extracts the token string

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
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM]) #Verifies the token and returns the payload

        #1️⃣ Receive token
        #2️⃣ Decode + verify signature using SECRET_KEY
        #3️⃣ Extract user_id from payload

        id = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception

    return token_data

# CHANGED: Function is now async def because it needs to await DB operations
# CHANGED: db parameter type from Session to AsyncSession
async def get_current_user(token : str = Depends(oauth2_scheme), db : AsyncSession = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = f"Could not validate Credentials", headers = {"WWW-Authenticate" : "Bearer"})

    # CHANGED: Added await — verify_access_token is async def, without await it returns a coroutine object
    # and never actually runs, causing a 500 error on all protected routes
    token_data = await verify_access_token(token , credentials_exception)

    # CHANGED: Using await db.execute(select().where()) instead of db.query().filter().first()
    # This is async and won't block other requests while waiting for DB response
    result = await db.execute(
        select(models.User)
        .where(models.User.id == token_data.id)
    )
    user = result.scalar_first()  # NEW: scalar_first() gets first result or None
    # OLD: user = db.query(models.User).filter(models.User.id == token_data.id).first()
    # OLD: This blocked the entire worker thread while waiting for DB

    return user

#Below is what jwttoken structure looks like
#Header:
#{
#  "alg": "HS256",
#  "typ": "JWT"
#}

#Payload:
#{
#  "id": 5,
#  "exp": 1699999999    ← expiry timestamp
#}

#Signature:
 # HMACSHA256(
 #   base64(header) + "." + base64(payload),
  #  your_secret_key         ← only your server knows this
  #)
