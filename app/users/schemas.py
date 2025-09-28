from typing import List
from pydantic import BaseModel, Field


class LocationIn(BaseModel):
    lat: str = Field(...)
    long: str = Field(...)


class OrderItemIn(BaseModel):
    itemId: str = Field(...)
    quantity: int = Field(..., ge=1)


class OrderIn(BaseModel):
    merchantId: str = Field(...)
    isStartingPoint: bool = Field(...)
    items: List[OrderItemIn]


class EstimateRequest(BaseModel):
    userLocation: LocationIn
    orders: List[OrderIn]


class EstimateResponse(BaseModel):
    totalPrice: int
    estimatedDeliveryTimeInMinutes: int
    calculatedEstimateId: str
