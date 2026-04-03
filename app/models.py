from .database import Base
from sqlalchemy import Column,Integer,String,text,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index = True)
    expense = Column(Integer, nullable=False)
    description = Column(String)
    mode = Column(String)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False , server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index = True)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False , server_default=text('now()'))
