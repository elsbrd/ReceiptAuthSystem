import datetime
from typing import Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.constants import PaymentType
from src.db.models.receipt import Receipt, ReceiptProduct
from src.domain.mappers import map_receipt_db_to_entity
from src.domain.models import ReceiptEntity


class ReceiptRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def save_receipt(self, receipt_entity: ReceiptEntity) -> ReceiptEntity:
        receipt_model_obj = Receipt(
            user_id=receipt_entity.user_id,
            total=receipt_entity.total,
            rest=receipt_entity.rest,
            payment_type=receipt_entity.payment.type,
            payment_amount=receipt_entity.payment.amount,
            products=[
                ReceiptProduct(
                    name=product.name,
                    price=product.price,
                    quantity=product.quantity,
                    total=product.total,
                )
                for product in receipt_entity.products
            ],
        )

        self.session.add(receipt_model_obj)
        self.session.commit()
        self.session.refresh(receipt_model_obj)

        return map_receipt_db_to_entity(receipt_model_obj)

    def get_receipt_by_id(self, receipt_id: int, user_id: int) -> ReceiptEntity | None:
        receipt_model_obj: Receipt | None = (
            self.session.query(Receipt)
            .filter(Receipt.id == receipt_id, Receipt.user_id == user_id)
            .first()
        )
        if not receipt_model_obj:
            return

        return map_receipt_db_to_entity(receipt_model_obj)

    def list_receipts(
        self,
        user_id: int,
        limit: int,
        offset: int,
        created_after: Optional[datetime.datetime],
        minimum_total: Optional[float],
        payment_type: Optional[PaymentType],
    ) -> Tuple[list[ReceiptEntity], int]:
        query = self.session.query(Receipt).filter(Receipt.user_id == user_id)

        if created_after:
            query = query.filter(Receipt.created_at >= created_after)

        if minimum_total:
            query = query.filter(Receipt.total >= minimum_total)

        if payment_type:
            query = query.filter(Receipt.payment_type == payment_type)

        total_count = int(query.with_entities(func.count()).scalar())

        receipt_db_models = query.limit(limit).offset(offset).all()

        receipts = [map_receipt_db_to_entity(r) for r in receipt_db_models]

        return receipts, total_count

    def get_receipt_by_public_id(self, public_id: str) -> ReceiptEntity | None:
        receipt_model_obj: Receipt | None = (
            self.session.query(Receipt).filter(Receipt.public_id == public_id).first()
        )
        if not receipt_model_obj:
            return

        return map_receipt_db_to_entity(receipt_model_obj)
