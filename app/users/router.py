from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dependencies import get_session
from app.estimate.schemas import EstimateRequest, EstimateResponse
from app.estimate.service import EstimateService
from app.merchants.enums import MerchantCategoryEnum
from app.orders.schemas import (
    OrderHistoryResponse,
    PlaceOrderRequest,
    PlaceOrderResponse,
)
from app.orders.service import OrderService

router = APIRouter(prefix="/api/v1", tags=["users"])


@router.post(
    "/users/estimate", response_model=EstimateResponse, status_code=status.HTTP_200_OK
)
async def post_users_estimate(
    body: EstimateRequest,
    session: AsyncSession = Depends(get_session),
    _=Depends(get_current_user),
):
    return await EstimateService.calculate(session, body)


@router.post(
    "/users/orders",
    response_model=PlaceOrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def place_order(
    body: PlaceOrderRequest,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    order_id = await OrderService.place_order_from_estimate(
        session, body.calculatedEstimateId, user
    )
    return PlaceOrderResponse(orderId=order_id)


@router.get(
    "/users/orders",
    response_model=List[OrderHistoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_orders(
    limit: int = Query(5, ge=0),
    offset: int = Query(0, ge=0),
    merchantId: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    merchantCategory: Optional[MerchantCategoryEnum] = Query(None),
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    results = await OrderService.list_user_orders(
        session=session,
        user=user,
        merchantId=merchantId,
        name=name,
        merchantCategory=merchantCategory,
        limit=limit,
        offset=offset,
    )
    return results
