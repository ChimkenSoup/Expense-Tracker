from passlib.context import CryptContext
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
#above code tells passlib what hashing algorithm we want to use,deprecated = auto will autohash if schmes is changed

def hash(password: str):
    return pwd_context.hash(password)

def verify_login(user_password, hashed_password):
    return pwd_context.verify(user_password,hashed_password)
#verfies the password
