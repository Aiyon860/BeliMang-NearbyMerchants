from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dependencies import get_session
from app.estimate.schemas import EstimateRequest, EstimateResponse
from app.estimate.service import EstimateService
from app.orders.schemas import PlaceOrderRequest, PlaceOrderResponse
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
    order_id = await OrderService.create_order(session, body.calculatedEstimateId, user)
    return PlaceOrderResponse(orderId=order_id)
