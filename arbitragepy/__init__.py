from decimal import Decimal

from .exchange_payload import ExchangePayload


def get_spread(ask_price: Decimal, bid_price: Decimal) -> Decimal:
    """Returns spread percent between `ask_price` and `bid_price` prices.

    Args:
        ask_price (Decimal): price for buy
        bid_price (Decimal): price for bought

    Returns:
        Decimal
    """

    return (bid_price / ask_price - 1) * 100


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


def plus_fee(n: Decimal, fee: Decimal) -> Decimal:
    """Returns the number from which, if you subtract the `fee` percent, you get `n`

    Args:
        n (Decimal)
        fee (Decimal): fee in percent which greater than 0

    Returns:
        Decimal
    """

    return n / (1 - fee / 100)


def minus_fee(n: Decimal, fee: Decimal) -> Decimal:
    """Returns the number to which, if you add the `fee` percent, you get `n`

    Args:
        n (Decimal)
        fee (Decimal): fee in percent which greater than 0

    Returns:
        Decimal
    """

    return n / (1 + fee / 100)
