from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CurrencyPayload:
    """Has data from order from exchange and about currency.

    Args:
        price (Decimal): currency price.
        quantity (Decimal): currency quantity.
        quantity_increment (Decimal): quantity increment.
        min_quantity (Decimal): min currency quantity.
        fee (Decimal): currency ask/bid fee in percent.
        ask_fee_in_base_currency (bool): True if exchange takes fee in base currency.
    """

    price: Decimal
    quantity: Decimal
    quantity_increment: Decimal
    min_quantity: Decimal = Decimal("0")
    fee: Decimal = Decimal("0")
    ask_fee_in_base_currency: bool = False
