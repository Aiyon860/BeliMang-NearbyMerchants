from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database import asyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with asyncSessionLocal() as session:
        yield session
