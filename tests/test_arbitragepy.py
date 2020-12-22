from decimal import Decimal

from arbitragepy import (get_spread, is_compatible_quantity_increments,
                         minus_fee, plus_fee, to_compatible_quantity_increment)


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


def test_to_compatible_quantity_increment() -> None:
    assert to_compatible_quantity_increment(
        Decimal("15"), Decimal("6")) == Decimal("12")
    assert to_compatible_quantity_increment(
        Decimal("15"), Decimal("3")) == Decimal("15")
    assert to_compatible_quantity_increment(
        Decimal("20"), Decimal("7")) == Decimal("14")


def test_plus_fee() -> None:
    assert plus_fee(Decimal("100"), Decimal("50")) == Decimal("200")
    assert plus_fee(Decimal("70"), Decimal("30")) == Decimal("100")


def test_minus_fee() -> None:
    assert minus_fee(Decimal("60"), Decimal("20")) == Decimal("50")
    assert minus_fee(Decimal("294.4"), Decimal("15")) == Decimal("256")
