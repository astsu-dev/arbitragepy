from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ExchangePayload:
    """This class represents exchange currency data for arbitrage comparison.
    
    Args:
        price (Decimal): currency price
        quantity (Decimal): currency quantity
        quantity_increment (Decimal): quantity increment step
        min_quantity (Decimal): min currency quantity
        commission (Decimal): currency ask/bid commission in percent
    """

    price: Decimal
    quantity: Decimal
    quantity_increment: Decimal
    min_quantity: Decimal = Decimal("0")
    commission: Decimal = Decimal("0")
