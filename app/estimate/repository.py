import uuid
from typing import Dict, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.merchants.models import Item, Merchant

from .models import Estimate


class EstimateRepository:
    @staticmethod
    async def get_merchants_by_ids(
        session: AsyncSession, merchant_ids: Iterable[str]
    ) -> Dict[str, Merchant]:
        stmt = select(Merchant).where(Merchant.id.in_(merchant_ids))
        result = await session.execute(stmt)
        merchants = result.scalars().all()
        return {str(merchant.id): merchant for merchant in merchants}

    @staticmethod
    async def get_items_by_merchant_and_item_ids(
        session: AsyncSession, merchant_id: str, item_ids: Iterable[str]
    ) -> Dict[str, Item]:
        stmt = select(Item).where(
            Item.merchant_id == merchant_id, Item.id.in_(item_ids)
        )
        result = await session.execute(stmt)
        items = result.scalars().all()
        return {str(item.id): item for item in items}

    @staticmethod
    async def save_estimate(
        session: AsyncSession, total_price: int, est_minutes: int
    ) -> str:
        eid = uuid.uuid4()
        est = Estimate(id=eid, total_price=total_price, est_minutes=est_minutes)
        session.add(est)
        await session.commit()
        return str(eid)
