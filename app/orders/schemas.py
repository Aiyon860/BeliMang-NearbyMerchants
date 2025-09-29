from pydantic import BaseModel, Field


class PlaceOrderRequest(BaseModel):
    calculatedEstimateId: str = Field(...)


class PlaceOrderResponse(BaseModel):
    orderId: str
