from collections.abc import Sequence
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import or_

from app.estimate.models import EstimateItem
from app.merchants.enums import MerchantCategoryEnum
from app.merchants.models import Item, Merchant

from .models import Order, OrderItem


class OrderRepository:
    @staticmethod
    async def create_order_from_estimate(
        session: AsyncSession, user_id: str, estimate_id: str
    ):
        # Create order
        order = Order(user_id=user_id, estimate_id=estimate_id)
        session.add(order)
        await session.flush()

        # Copy from estimate items to order items
        stmt = select(EstimateItem).where(EstimateItem.estimate_id == estimate_id)
        result = await session.execute(stmt)
        est_items = result.scalars().all()

        items_rows = []
        for ei in est_items:
            oi = OrderItem(
                order_id=order.id,
                item_id=ei.item_id,
                quantity=ei.quantity,
                price=ei.unit_price,
            )
            items_rows.append(oi)
        session.add_all(items_rows)

        return str(order.id)

    @staticmethod
    async def fetch_orders_for_user(
        session: AsyncSession,
        user_id: str,
        merchant_id: Optional[str] = None,
        name: Optional[str] = None,
        merchant_category: Optional[MerchantCategoryEnum] = None,
        limit: int = 5,
        offset: int = 0,
    ) -> Sequence[Order]:
        # Base query: orders for user
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(
                selectinload(Order.order_items)
                .selectinload(OrderItem.item)
                .selectinload(Item.merchant)
            )
            .order_by(Order.created_at.desc())
        )

        # If name or merchant_category filters exist, we need to join to those tables
        # Build join-based filters to avoid loading unrelated orders
        if merchant_id or name or merchant_category:
            # join through relationships
            stmt = stmt.join(Order.order_items).join(OrderItem.item).join(Item.merchant)

            if merchant_id:
                stmt = stmt.where(Item.merchant_id == merchant_id)

            if merchant_category:
                stmt = stmt.where(Merchant.merchant_category == merchant_category)

            if name:
                pattern = f"%{name}%"
                stmt = stmt.where(
                    or_(Merchant.name.ilike(pattern), Item.name.ilike(pattern))
                )

            # distinct orders to avoid duplicates due to join
            stmt = stmt.distinct()

        # Pagination
        stmt = stmt.limit(limit).offset(offset)

        result = await session.execute(stmt)
        orders = result.scalars().unique().all()
        return orders
