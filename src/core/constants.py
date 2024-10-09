from enum import Enum as PyEnum


class PaymentType(str, PyEnum):
    CASH = "cash"
    CARD = "card"
