from datetime import datetime
from typing import List
import uuid

from geoalchemy2 import Geography
from sqlalchemy import (
    UUID,
    Integer,
    String,
    Float,
    DateTime,
    Enum,
    func,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base
from enums import MerchantCategoryEnum


class Merchant(Base):
    __tablename__ = "merchants"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    merchant_category: Mapped[MerchantCategoryEnum] = mapped_column(
        Enum(MerchantCategoryEnum, name="merchant_category_enum", create_type=False),
        nullable=False,
    )
    image_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    geog: Mapped[Geography] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    items: Mapped[List["Item"]] = relationship(
        "Item", back_populates="merchant", lazy="selectin"
    )


class Item(Base):
    __tablename__ = "items"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("merchants.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    merchant: Mapped["Merchant"] = relationship(
        "Merchant", back_populates="items", primaryjoin="Item.merchant_id==Merchant.id"
    )
