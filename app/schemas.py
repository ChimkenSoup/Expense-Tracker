from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class ExpenseBase(BaseModel):
    expense : int
    description : Optional[str] = None
    mode : Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime
    owner_id : int

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None

