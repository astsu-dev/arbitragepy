from decimal import Decimal


def get_spread(ask_price: Decimal, bid_price: Decimal) -> Decimal:
    """Returns spread percent between `ask_price` and `bid_price` prices.

    Args:
        ask_price (Decimal): price for buy
        bid_price (Decimal): price for bought

    Returns:
        Decimal
    """

    return (bid_price / ask_price - 1) * 100
