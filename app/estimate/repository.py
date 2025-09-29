import uuid
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import insert
from sqlalchemy.sql.expression import select

from .models import Estimate, EstimateItem


class EstimateRepository:
    @staticmethod
    async def save_estimate(
        session: AsyncSession, total_price: int, est_minutes: int
    ) -> str:
        eid = uuid.uuid4()
        est = Estimate(id=eid, total_price=total_price, est_minutes=est_minutes)
        session.add(est)
        await session.flush()  # Ensure both estimate and its items are saved
        return str(eid)

    @staticmethod
    async def bulk_insert_estimate_items(
        session: AsyncSession, rows: List[Dict]
    ) -> None:
        await session.execute(insert(EstimateItem), rows)

    @staticmethod
    async def get_estimate_with_items(
        session: AsyncSession,
        estimate_id: str,
    ):
        q = (
            select(Estimate)
            .where(Estimate.id == estimate_id)
            .options(
                selectinload(Estimate.items)
            )  # relationship Estimate.items -> list[EstimateItem]
        )
        res = await session.execute(q)
        return res.scalars().first()
