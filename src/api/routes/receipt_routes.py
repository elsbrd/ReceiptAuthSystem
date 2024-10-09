import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import PlainTextResponse

from src.core.constants import PaymentType
from src.db.models.user import User
from src.dependencies.auth import get_current_user
from src.dependencies.receipt import get_receipt_service
from src.schemas.receipt import (
    PaginatedReceiptResponseSchema,
    ReceiptCreateSchema,
    ReceiptResponseSchema,
)
from src.services.receipt import ReceiptService
from src.services.receipt_formatting import generate_receipt_text

router = APIRouter()


@router.post(
    "/receipts",
    response_model=ReceiptResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_receipt(
    receipt_data: ReceiptCreateSchema,
    receipt_service: ReceiptService = Depends(get_receipt_service),
    current_user: User = Depends(get_current_user),
):
    receipt = receipt_service.create_receipt(receipt_data.dict(), current_user.id)
    return receipt.to_dict()


@router.get("/receipts/{receipt_id}", response_model=ReceiptResponseSchema)
def get_receipt_by_id(
    receipt_id: int,
    receipt_service: ReceiptService = Depends(get_receipt_service),
    current_user: User = Depends(get_current_user),
):
    receipt = receipt_service.get_receipt_by_id(
        receipt_id=receipt_id, user_id=current_user.id
    )

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return receipt.to_dict()


@router.get("/receipts", response_model=PaginatedReceiptResponseSchema)
def list_receipts(
    receipt_service: ReceiptService = Depends(get_receipt_service),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    created_after: Optional[datetime.datetime] = None,
    minimum_total: Optional[float] = None,
    payment_type: Optional[PaymentType] = None,
):
    receipts, total_count = receipt_service.list_receipts(
        user_id=current_user.id,
        limit=limit,
        offset=offset,
        created_after=created_after,
        minimum_total=minimum_total,
        payment_type=payment_type,
    )

    return {"receipts": [r.to_dict() for r in receipts], "total_count": total_count}


@router.get("/receipts/{public_id}/view", response_class=PlainTextResponse)
def view_receipt_by_public_id(
    public_id: str,
    line_length: Optional[int] = Query(32),
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> str:
    receipt = receipt_service.view_receipt_by_public_id(public_id=public_id)

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return generate_receipt_text(receipt, line_length)
