from decimal import Decimal


def is_compatible_quantity_increments(qty_inc1: Decimal, qty_inc2: Decimal) -> bool:
    """Returns True if `qty_inc1` % `qty_inc2` == 0 or `qty_inc2` % `qty_inc1` == 0

    Args:
        qty_inc1 (Decimal)
        qty_inc2 (Decimal)

    Returns:
        bool
    """

    return qty_inc1 % qty_inc2 == 0 or qty_inc2 % qty_inc1 == 0


def to_compatible_quantity_increment(n: Decimal, qty_inc: Decimal) -> Decimal:
    """Converts `n` to number which devided on `qty_inc`.

    Args:
        n (Decimal)
        qty_inc (Decimal): quantity increment

    Returns:
        Decimal
    """

    return n // qty_inc * qty_inc
