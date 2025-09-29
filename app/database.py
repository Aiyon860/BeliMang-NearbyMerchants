import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:root@localhost/merchants_db"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
asyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, autoflush=True, autocommit=False
)
Base = declarative_base()
