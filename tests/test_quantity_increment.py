from decimal import Decimal

from arbitrageutils import (is_compatible_quantity_increments,
                            to_compatible_quantity_increment)


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


# TODO Test validate_quantity_increments.
