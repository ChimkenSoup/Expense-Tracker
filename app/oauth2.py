from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker,Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')
#TElls the api about the login endpoint
#oauth2_scheme extracts the token string

SECRET_KEY = "D/wF84mYt3AMyKppbQ3RIrOKNQxgvCl+Le3v48kXa4o="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data : dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str , credentials_exception):
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
    
def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = f"Could not validate Credentials", headers = {"WWW-Authenticate" : "Bearer"})

    token_data = verify_access_token(token , credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

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