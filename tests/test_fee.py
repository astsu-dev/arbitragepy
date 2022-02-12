from decimal import Decimal

from arbitragepy.fee import minus_fee, plus_fee


def test_plus_fee() -> None:
    assert plus_fee(Decimal("100"), Decimal("50")) == Decimal("200")
    assert plus_fee(Decimal("70"), Decimal("30")) == Decimal("100")


def test_minus_fee() -> None:
    assert minus_fee(Decimal("60"), Decimal("20")) == Decimal("50")
    assert minus_fee(Decimal("294.4"), Decimal("15")) == Decimal("256")
