from sqlalchemy.orm import configure_mappers, relationship

from app.estimate.models import Estimate, EstimateItem
from app.merchants.models import Item, Merchant
from app.orders.models import Order, OrderItem
from app.users.models import User

if not hasattr(User, "orders"):
    User.orders = relationship("Order", back_populates="user", lazy="selectin")
if not hasattr(Order, "user"):
    Order.user = relationship("User", back_populates="orders")
if not hasattr(Order, "estimate"):
    Order.estimate = relationship("Estimate", lazy="selectin")

configure_mappers()

__all__ = ["User", "Order", "Estimate", "Merchant", "Item", "OrderItem", "EstimateItem"]
