import uuid

from sqlalchemy import UUID, Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.constants import PaymentType
from src.db.session import Base


class Receipt(Base):
    __tablename__ = "receipt"

    id = Column(Integer, primary_key=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Float)
    rest = Column(Float)
    payment_type = Column(Enum(PaymentType))
    payment_amount = Column(Float)

    products = relationship("ReceiptProduct", back_populates="receipt")


class ReceiptProduct(Base):
    __tablename__ = "receipt_product"

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipt.id"))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    total = Column(Float)

    receipt = relationship("Receipt", back_populates="products")
