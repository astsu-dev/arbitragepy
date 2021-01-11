from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CurrencyPayload:
    """This dataclass represents exchange currency data for arbitrage comparison.

    Args:
        price (Decimal): currency price
        quantity (Decimal): currency quantity
        quantity_increment (Decimal): quantity increment step
        min_quantity (Decimal): min currency quantity
        fee (Decimal): currency ask/bid fee in percent
        ask_fee_in_base_currency (bool)
    """

    price: Decimal
    quantity: Decimal
    quantity_increment: Decimal
    min_quantity: Decimal = Decimal("0")
    fee: Decimal = Decimal("0")
    ask_fee_in_base_currency: bool = False
