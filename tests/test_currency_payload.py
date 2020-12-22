from decimal import Decimal

from arbitrageutils import CurrencyPayload


def test_currency_payload() -> None:
    p = CurrencyPayload(
        price=Decimal("100.15"),
        quantity=Decimal("200.002"),
        quantity_increment=Decimal("0.001"))
    assert p.price == Decimal("100.15")
    assert p.quantity == Decimal("200.002")
    assert p.quantity_increment == Decimal("0.001")
    assert p.min_quantity == Decimal("0")
    assert p.commission == Decimal("0")
    assert not p.ask_commission_in_current_currency

    p = CurrencyPayload(
        price=Decimal("100.15"),
        quantity=Decimal("200.002"),
        quantity_increment=Decimal("0.001"),
        min_quantity=Decimal("1.10"),
        commission=Decimal("1"),
        ask_commission_in_current_currency=True)
    assert p.min_quantity == Decimal("1.10")
    assert p.commission == Decimal("1")
    assert p.ask_commission_in_current_currency
