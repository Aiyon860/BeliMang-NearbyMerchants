from typing import Optional
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2 import functions as geofunc

from models import Merchant, Item
from enums import MerchantCategoryEnum


class MerchantRepository:
    @staticmethod
    async def get_nearby_merchants(
        session: AsyncSession,
        lat: float,
        long: float,
        merchantId: Optional[str],
        merchantCategory: Optional[str],
        name: Optional[str],
        limit: int,
        offset: int,
    ):
        stmt = select(Merchant)

        if merchantId:
            stmt = stmt.where(Merchant.id == merchantId)

        if merchantCategory:
            stmt = stmt.where(
                Merchant.merchant_category == MerchantCategoryEnum[merchantCategory]
            )

        if name:
            stmt = stmt.join(Merchant.items).where(
                or_(Merchant.name.ilike(f"%{name}%"), Item.name.ilike(f"%{name}%"))
            )

        stmt = (
            stmt.order_by(
                geofunc.ST_Distance(
                    Merchant.geog,
                    func.ST_SetSRID(func.ST_MakePoint(long, lat), 4326),
                )
            )
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(stmt)
        return result.scalars().unique().all()
