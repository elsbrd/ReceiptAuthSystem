import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, confloat, conint, conlist


class ProductCreateSchema(BaseModel):
    name: str
    price: confloat(ge=0)
    quantity: conint(gt=0)


class PaymentSchema(BaseModel):
    amount: confloat(gt=0)
    type: str


class ReceiptCreateSchema(BaseModel):
    products: List[ProductCreateSchema]
    payment: PaymentSchema


class ReceiptResponseSchema(BaseModel):
    id: int
    public_id: UUID
    total: float
    rest: float
    payment: dict
    products: List[dict]
    created_at: datetime.datetime


class PaginatedReceiptResponseSchema(BaseModel):
    receipts: List[ReceiptResponseSchema]
    total_count: int
