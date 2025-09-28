from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from enums import MerchantCategoryEnum


class LocationSchema(BaseModel):
    lat: float
    long: float


class ItemResponse(BaseModel):
    itemId: str = Field(..., alias="itemId")
    name: str
    price: int


class DetailMerchantResponse(BaseModel):
    merchantId: str = Field(..., alias="merchantId")
    name: str
    merchantCategory: MerchantCategoryEnum
    imageUrl: str
    location: LocationSchema
    createdAt: datetime


class MerchantResponse(BaseModel):
    merchant: DetailMerchantResponse
    items: List[ItemResponse]


class NearbyResponse(BaseModel):
    data: List[MerchantResponse]
    meta: dict
