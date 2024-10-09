import datetime
from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.core.constants import PaymentType


@dataclass
class ProductEntity:
    name: str
    price: float
    quantity: int

    @property
    def total(self) -> float:
        return self.price * self.quantity

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "total": self.total,
        }


@dataclass
class PaymentEntity:
    amount: float
    type: str

    def to_dict(self) -> dict:
        return {"type": self.type, "amount": self.amount}


@dataclass
class ReceiptEntity:
    user_id: int
    products: List[ProductEntity]
    payment: PaymentEntity
    total: float = 0
    rest: float = 0
    id: int | None = None
    public_id: UUID | None = None
    created_at: datetime.datetime | None = None

    def calculate_total(self):
        self.total = sum(product.total for product in self.products)
        self.rest = (
            self.payment.amount - self.total
            if self.payment.type == PaymentType.CASH
            else 0
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "public_id": self.public_id,
            "total": self.total,
            "rest": self.rest,
            "products": [product.to_dict() for product in self.products],
            "payment": self.payment.to_dict(),
            "created_at": self.created_at,
        }
