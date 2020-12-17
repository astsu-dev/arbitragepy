from decimal import Decimal

from arbitragepy import ExchangePayload


def test_exchange_payload() -> None:
    p = ExchangePayload(
        price=Decimal("100.15"),
        quantity=Decimal("200.002"),
        quantity_increment=Decimal("0.001"))
    assert p.price == Decimal("100.15")
    assert p.quantity == Decimal("200.002")
    assert p.quantity_increment == Decimal("0.001")
    assert p.min_quantity == Decimal("0")

    p = ExchangePayload(
        price=Decimal("100.15"),
        quantity=Decimal("200.002"),
        quantity_increment=Decimal("0.001"),
        min_quantity=Decimal("1.10"))
    assert p.min_quantity == Decimal("1.10")
