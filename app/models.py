from .database import Base
from sqlalchemy import Column,Integer,String,text,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index = True)
    expense = Column(Integer, nullable=False)
    description = Column(String(255))
    mode = Column(String(50))
    created_at = Column(TIMESTAMP, nullable = False , server_default=text('CURRENT_TIMESTAMP'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index = True)
    email = Column(String(255), nullable = False, unique = True)
    password = Column(String(255), nullable = False)
    created_at = Column(TIMESTAMP, nullable = False , server_default=text('CURRENT_TIMESTAMP'))

