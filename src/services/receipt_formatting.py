from src.core.constants import PaymentType
from src.domain.models import ReceiptEntity


def generate_receipt_text(receipt: ReceiptEntity, line_length: int = 32) -> str:
    def center_text(text: str) -> str:
        return text.center(line_length)

    def format_quantity_price_line(quantity: float, price: float) -> str:
        return f"{quantity:.2f} x {price:,.2f}".replace(",", " ").ljust(line_length)

    def format_product_name_line(product_name: str, total: float) -> str:
        words = product_name.split()
        product_lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= line_length // 2:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                product_lines.append(current_line)
                current_line = word

        if current_line:
            product_lines.append(current_line)

        product_lines[-1] = f"{product_lines[-1]}".ljust(
            line_length // 2
        ) + f"{total:,.2f}".replace(",", " ").rjust(line_length // 2)

        return "\n".join(product_lines)

    def format_total(label: str, value: float) -> str:
        return f"{label}".ljust(line_length // 2) + f"{value:,.2f}".replace(
            ",", " "
        ).rjust(line_length // 2)

    lines = [center_text("ФОП Джонсонюк Борис"), "=" * line_length]

    for index, product in enumerate(receipt.products):
        lines.append(format_quantity_price_line(product.quantity, product.price))
        lines.append(format_product_name_line(product.name, product.total))
        if index < len(receipt.products) - 1:
            lines.append("-" * line_length)

    lines.append("=" * line_length)
    lines.append(format_total("СУМА", receipt.total))
    lines.append(
        format_total(
            "Картка" if receipt.payment.type == PaymentType.CARD else "Готівка",
            receipt.payment.amount,
        )
    )
    lines.append(format_total("Решта", receipt.rest))
    lines.append("=" * line_length)
    lines.append(center_text(receipt.created_at.strftime("%d.%m.%Y %H:%M")))
    lines.append(center_text("Дякуємо за покупку!"))

    return "\n".join(lines)
