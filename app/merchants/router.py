from typing import Optional
from fastapi import Depends, Path, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_session
from .schemas import NearbyResponse
from .service import MerchantService

router = APIRouter(prefix="/api/v1", tags=["merchants"])


@router.get("/merchants/nearby/{lat},{long}", response_model=NearbyResponse)
async def get_nearby(
    lat=Path(...),
    long=Path(...),
    merchantId: Optional[str] = Query(None),
    limit: int = Query(5),
    offset: int = Query(0),
    name: Optional[str] = Query(None),
    merchantCategory: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    return await MerchantService.get_nearby_merchants(
        session, lat, long, merchantId, merchantCategory, name, limit, offset
    )
