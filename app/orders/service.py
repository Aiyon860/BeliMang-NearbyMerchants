from collections.abc import Sequence
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.estimate.repository import EstimateRepository
from app.merchants.enums import MerchantCategoryEnum
from app.merchants.repository import MerchantRepository
from app.merchants.schemas import (
    DetailMerchantResponse,
    ItemResponse,
    LocationSchema,
    MerchantResponse,
)
from app.users.models import User

from .models import Order
from .repository import OrderRepository
from .schemas import OrderHistoryResponse


class OrderService:
    @staticmethod
    async def place_order_from_estimate(
        session: AsyncSession, estimate_id: str, user: User
    ) -> str:
        # Check estimate id exist or not
        estimate = await EstimateRepository.get_estimate_with_items(
            session, estimate_id
        )
        if not estimate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estimate id not found",
            )

        order_id = await OrderRepository.create_order_from_estimate(
            session, str(user.id), str(estimate.id)
        )
        await session.commit()
        return order_id

    @staticmethod
    async def list_user_orders(
        session: AsyncSession,
        user: User,
        merchantId: Optional[str] = None,
        name: Optional[str] = None,
        merchantCategory: Optional[MerchantCategoryEnum] = None,
        limit: int = 5,
        offset: int = 0,
    ):
        if merchantId:
            # Validate UUID format
            try:
                UUID(merchantId)
            except ValueError:
                return []

            m = await MerchantRepository.get_merchant_by_id(session, merchantId)
            # Validate merchantId
            if not m:
                return []

            # Validate category
            if (
                merchantCategory
                and merchantCategory not in MerchantCategoryEnum.__members__
            ):
                return []

        # Fetch orders
        orders: Sequence[Order] = await OrderRepository.fetch_orders_for_user(
            session=session,
            user_id=str(user.id),
            merchant_id=merchantId,
            name=name,
            merchant_category=merchantCategory,
            limit=limit,
            offset=offset,
        )

        pattern_lower = name.casefold() if name else None

        # Format response
        data = []
        for ord in orders:
            # Group order items by merchant
            merchant_map = {}  # merchant_id -> {"merchant":..., "items":[...]}
            for oi in ord.order_items:
                item = oi.item
                merchant = item.merchant

                # Filter by merchantId
                if merchantId and str(merchantId) != str(merchant.id):
                    continue

                # Filter by merchantCategory
                if merchantCategory and merchantCategory != merchant.merchant_category:
                    continue

                # Filter by merchant or item name
                if pattern_lower:
                    merchant_name_cf = merchant.name.casefold()
                    item_name_cf = item.name.casefold()
                    if (
                        pattern_lower not in merchant_name_cf
                        and pattern_lower not in item_name_cf
                    ):
                        continue

                mid = str(merchant.id)
                if mid not in merchant_map:
                    merchant_map[mid] = MerchantResponse(
                        merchant=DetailMerchantResponse(
                            merchantId=str(merchant.id),
                            name=merchant.name,
                            merchantCategory=merchant.merchant_category,
                            imageUrl=HttpUrl(merchant.image_url),
                            location=LocationSchema(
                                lat=merchant.latitude, long=merchant.longitude
                            ),
                            createdAt=merchant.created_at.isoformat(),
                        ),
                        items=[],
                    )
                merchant_map[mid].items.append(
                    ItemResponse(
                        itemId=str(item.id),
                        name=item.name,
                        productCategory=item.product_category,
                        imageUrl=HttpUrl(item.image_url),
                        price=oi.price,
                        quantity=oi.quantity,
                        createdAt=item.created_at.isoformat(),
                    )
                )

            merchant_entries = list(merchant_map.values())
            data.append(
                OrderHistoryResponse(orderId=str(ord.id), orders=merchant_entries)
            )

        return data
