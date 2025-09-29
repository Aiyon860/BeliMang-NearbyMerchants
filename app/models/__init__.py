from sqlalchemy.orm import configure_mappers

from app.estimate.models import Estimate
from app.merchants.models import Item, Merchant
from app.orders.models import Order
from app.users.models import User
from sqlalchemy.orm import relationship

if not hasattr(User, "orders"):
    User.orders = relationship("Order", back_populates="user", lazy="selectin")
if not hasattr(Order, "user"):
    Order.user = relationship("User", back_populates="orders")
if not hasattr(Order, "estimate"):
    Order.estimate = relationship("Estimate", lazy="selectin")

configure_mappers()

__all__ = ["User", "Order", "Estimate", "Merchant", "Item"]
