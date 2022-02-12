from decimal import Decimal

from arbitragepy.spread import get_spread


def test_get_spread() -> None:
    assert get_spread(Decimal("100"), Decimal("200")) == Decimal("100")
    assert get_spread(Decimal("200"), Decimal("100")) == Decimal("-50")
    assert get_spread(Decimal("0.5"), Decimal("2.0")) == Decimal("300")
    assert get_spread(Decimal("0.5"), Decimal("0.75")) == Decimal("50")
