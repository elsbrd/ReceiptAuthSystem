from src.db.models.receipt import Receipt
from src.domain.models import PaymentEntity, ProductEntity, ReceiptEntity


def map_receipt_db_to_entity(receipt_db_obj: Receipt) -> ReceiptEntity:
    return ReceiptEntity(
        id=receipt_db_obj.id,
        public_id=receipt_db_obj.public_id,
        user_id=receipt_db_obj.user_id,
        products=[
            ProductEntity(name=p.name, price=p.price, quantity=p.quantity)
            for p in receipt_db_obj.products
        ],
        payment=PaymentEntity(
            amount=receipt_db_obj.payment_amount, type=receipt_db_obj.payment_type
        ),
        total=receipt_db_obj.total,
        rest=receipt_db_obj.rest,
        created_at=receipt_db_obj.created_at,
    )
