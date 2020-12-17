from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ExchangePayload:
    """This class represents exchange currency data for arbitrage comparison."""

    price: Decimal
    quantity: Decimal
    quantity_increment: Decimal
    min_quantity: Decimal = Decimal("0")
