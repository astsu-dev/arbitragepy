from decimal import Decimal

from arbitragepy import get_spread, is_compatible_quantity_increments


def test_get_spread() -> None:
    assert get_spread(Decimal("100"), Decimal("200")) == Decimal("100")
    assert get_spread(Decimal("200"), Decimal("100")) == Decimal("-50")
    assert get_spread(Decimal("0.5"), Decimal("2.0")) == Decimal("300")
    assert get_spread(Decimal("0.5"), Decimal("0.75")) == Decimal("50")


def test_is_compatible_quantity_increments() -> None:
    assert is_compatible_quantity_increments(Decimal("4"), Decimal("2"))
    assert is_compatible_quantity_increments(Decimal("2"), Decimal("4"))

    assert is_compatible_quantity_increments(Decimal("5"), Decimal("0.1"))
    assert is_compatible_quantity_increments(Decimal("0.1"), Decimal("5"))

    assert is_compatible_quantity_increments(Decimal("0.99"), Decimal("0.11"))
    assert is_compatible_quantity_increments(Decimal("0.11"), Decimal("0.99"))

    assert is_compatible_quantity_increments(Decimal("1"), Decimal("0.001"))
    assert is_compatible_quantity_increments(Decimal("0.001"), Decimal("1"))

    assert not is_compatible_quantity_increments(
        Decimal("0.99"), Decimal("0.1"))
    assert not is_compatible_quantity_increments(
        Decimal("0.1"), Decimal("0.99"))

    assert not is_compatible_quantity_increments(Decimal("5"), Decimal("3"))
    assert not is_compatible_quantity_increments(Decimal("3"), Decimal("5"))
