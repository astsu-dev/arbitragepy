"""Has functions that make it easy to work with arbitrage mathematics."""

from .currency_payload import CurrencyPayload
from .exceptions import ImcompabileQuantityIncrementsError
from .fee import minus_fee, plus_fee
from .order_data import (OrderData, OrderPayload, OrdersData,
                         create_ask_order_data, create_bid_order_data,
                         create_orders_data)
from .quantity_increment import (is_compatible_quantity_increments,
                                 to_compatible_quantity_increment,
                                 validate_quantity_increments)
from .spread import get_spread
