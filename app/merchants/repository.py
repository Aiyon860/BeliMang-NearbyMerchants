from typing import Optional

from fastapi.param_functions import Depends
from geoalchemy2 import functions as geofunc
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_session

from .enums import MerchantCategoryEnum
from .models import Item, Merchant


class MerchantRepository:
    @staticmethod
    async def get_nearby_merchants(
        lat: float,
        long: float,
        merchantId: Optional[str],
        merchantCategory: Optional[str],
        name: Optional[str],
        limit: int,
        offset: int,
        session: AsyncSession = Depends(get_session),
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
