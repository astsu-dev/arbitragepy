from dataclasses import dataclass
from decimal import Decimal

from .currency_payload import CurrencyPayload
from .exceptions import ImcompabileQuantityIncrementsError
from .fee import minus_fee, plus_fee
from .quantity_increment import (is_compatible_quantity_increments,
                                 to_compatible_quantity_increment,
                                 validate_quantity_increments)
from .spread import get_spread


@dataclass(frozen=True)
class OrderData:
    price: Decimal
    quantity: Decimal
    estimated_value: Decimal


@dataclass(frozen=True)
class OrdersData:
    ask: OrderData
    bid: OrderData
    spread: Decimal


@dataclass(frozen=True)
class OrderPayload:
    price: Decimal
    quantity: Decimal
    quantity_increment: Decimal
    fee: Decimal
    ask_fee_in_current_currency: bool = False


def create_orders_data(*, ask_currency_payload: CurrencyPayload,
                       bid_currency_payload: CurrencyPayload,
                       make_compatible_quantity_increments: bool = True
                       ) -> OrdersData:
    ask_price = ask_currency_payload.price
    bid_price = bid_currency_payload.price
    ask_cp_qty_inc = ask_currency_payload.quantity_increment
    bid_cp_qty_inc = bid_currency_payload.quantity_increment

    if make_compatible_quantity_increments:
        validate_quantity_increments(ask_cp_qty_inc, bid_cp_qty_inc)
        ask_qty_inc = bid_qty_inc = min(
            ask_cp_qty_inc, bid_cp_qty_inc)
    else:
        ask_qty_inc = ask_cp_qty_inc
        bid_qty_inc = bid_cp_qty_inc

    ask_quantity = bid_quantity = min(
        ask_currency_payload.quantity, ask_currency_payload.min_quantity,
        bid_currency_payload.quantity, bid_currency_payload.min_quantity)

    ask_order_payload = OrderPayload(
        ask_price, ask_quantity, ask_qty_inc, ask_currency_payload.fee,
        ask_currency_payload.ask_fee_in_current_currency)
    bid_order_payload = OrderPayload(
        bid_price, bid_quantity, bid_qty_inc, bid_currency_payload.fee,
        bid_currency_payload.ask_fee_in_current_currency)

    ask_order_data = create_ask_order_data(ask_order_payload)
    bid_order_data = create_bid_order_data(bid_order_payload)
    spread = get_spread(ask_price, bid_price)

    return OrdersData(ask_order_data, bid_order_data, spread)


def create_ask_order_data(order_payload: OrderPayload) -> OrderData:
    """Creates ask order data from `order_payload`.

    Makes currency quantity from `order_payload` compatible with quantity increment.
    Calculates currency estimated value.

    Args:
        order_payload (OrderPayload): payload for creating ask order data.

    Returns:
        OrderData
    """

    price = order_payload.price
    qty = order_payload.quantity
    qty_inc = order_payload.quantity_increment
    fee = order_payload.fee

    qty = to_compatible_quantity_increment(qty, qty_inc)

    if order_payload.ask_fee_in_current_currency:
        qty = to_compatible_quantity_increment(
            plus_fee(qty, fee), qty_inc)
        estimated_value = qty * price
    else:
        estimated_value = plus_fee(qty * price, fee)

    return OrderData(price=price, quantity=qty, estimated_value=estimated_value)


def create_bid_order_data(order_payload: OrderPayload) -> OrderData:
    """Creates bid order data from `order_payload`.

    Makes currency quantity from `order_payload` compatible with quantity increment.
    Calculates currency estimated value.

    Args:
        order_payload (OrderPayload): payload for creating bid order data.

    Returns:
        OrderData
    """

    price = order_payload.price
    qty = order_payload.quantity
    qty_inc = order_payload.quantity_increment
    fee = order_payload.fee

    qty = to_compatible_quantity_increment(qty, qty_inc)

    estimated_value = plus_fee(qty * price, fee)

    return OrderData(price=price, quantity=qty, estimated_value=estimated_value)
