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

#We can have different schemas for the different crud functions depending on the need.

#Below are the response models. point of response model is to show the caller what was actually saved to the database
#we return the attributes of the table

class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime
    owner_id : int

    class Config:
        from_attributes = True
        #Above line is to convert the sqlalchemy model to a pydantic model

class UserResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True

#Below are for login
#If anything is returned, it is good practice to setup a schema for it

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None
  