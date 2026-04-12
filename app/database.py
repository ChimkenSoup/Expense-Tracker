from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from asyncpg import Connection
from uuid import uuid4
from . import config
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"{settings.database_url}"

class UniqueNameConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4().hex}__"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "connection_class": UniqueNameConnection,
        "statement_cache_size": 0,
    }
)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
