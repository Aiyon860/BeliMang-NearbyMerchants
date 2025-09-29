from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.orders.repository import OrderRepository
from app.users.models import User


class OrderService:
    @staticmethod
    async def create_order(
        session: AsyncSession, estimate_id: str, user: User = Depends(get_current_user)
    ) -> str:
        estimate = await OrderRepository.get_estimate_by_id(session, estimate_id)
        if not estimate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estimate id not found",
            )
        order_id = await OrderRepository.create_order(
            session, str(user.id), estimate_id
        )
        return order_id
