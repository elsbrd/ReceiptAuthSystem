import datetime
from typing import Dict, Optional, Tuple

from sqlalchemy.orm import Session

from src.core.constants import PaymentType
from src.domain.models import PaymentEntity, ProductEntity, ReceiptEntity
from src.repositories.receipt_repository import ReceiptRepository


class ReceiptService:
    @classmethod
    def create(cls, db_session: Session) -> "ReceiptService":
        return cls(ReceiptRepository(db_session))

    def __init__(self, receipt_repository: ReceiptRepository):
        self.__receipt_repository = receipt_repository

    def create_receipt(self, receipt_data: Dict, user_id: int) -> ReceiptEntity:
        products = [
            ProductEntity(**product_data) for product_data in receipt_data["products"]
        ]
        payment = PaymentEntity(**receipt_data["payment"])

        receipt = ReceiptEntity(user_id=user_id, products=products, payment=payment)

        receipt.calculate_total()

        saved_receipt = self.__receipt_repository.save_receipt(receipt)

        return saved_receipt

    def get_receipt_by_id(self, receipt_id: int, user_id: int) -> ReceiptEntity:
        return self.__receipt_repository.get_receipt_by_id(receipt_id, user_id)

    def list_receipts(
        self,
        user_id: int,
        limit: int,
        offset: int,
        created_after: Optional[datetime.datetime],
        minimum_total: Optional[float],
        payment_type: Optional[PaymentType],
    ) -> Tuple[list[ReceiptEntity], int]:
        return self.__receipt_repository.list_receipts(
            user_id=user_id,
            limit=limit,
            offset=offset,
            created_after=created_after,
            minimum_total=minimum_total,
            payment_type=payment_type,
        )

    def view_receipt_by_public_id(self, public_id: str) -> ReceiptEntity | None:
        return self.__receipt_repository.get_receipt_by_public_id(public_id)
