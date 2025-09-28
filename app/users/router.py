from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_session
from .schemas import EstimateRequest, EstimateResponse
from .service import EstimateService

router = APIRouter(prefix="/api/v1", tags=["users"])


@router.post("/users/estimate", response_model=EstimateResponse)
async def post_users_estimate(
    body: EstimateRequest,
    session: AsyncSession = Depends(get_session),
):
    return await EstimateService.calculate(session, body)
