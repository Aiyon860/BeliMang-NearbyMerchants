from typing import List

from pydantic import BaseModel, Field

from app.merchants.schemas import MerchantResponse


class PlaceOrderRequest(BaseModel):
    calculatedEstimateId: str = Field(...)


class PlaceOrderResponse(BaseModel):
    orderId: str


class OrderHistoryResponse(BaseModel):
    orderId: str
    orders: List[MerchantResponse]
