from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
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


async def get_db():
    db = asyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
