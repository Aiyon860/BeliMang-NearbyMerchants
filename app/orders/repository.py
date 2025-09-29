import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.estimate.models import Estimate
from app.orders.models import Order


class OrderRepository:
    @staticmethod
    async def get_estimate_by_id(
        session: AsyncSession, estimate_id: str
    ) -> Optional[Estimate]:
        stmt = select(Estimate).where(Estimate.id == estimate_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def create_order(
        session: AsyncSession, user_id: str, estimate_id: str
    ) -> str:
        oid = uuid.uuid4()
        order = Order(id=oid, user_id=user_id, estimate_id=estimate_id)
        session.add(order)
        await session.commit()
        return str(oid)
