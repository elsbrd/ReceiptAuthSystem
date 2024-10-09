from fastapi import Depends
from sqlalchemy.orm import Session

from src.dependencies.db import get_db_session
from src.services.receipt import ReceiptService


def get_receipt_service(
    db_session: Session = Depends(get_db_session),
) -> ReceiptService:
    return ReceiptService.create(db_session)
