"""Has functions for work with orders."""

from dataclasses import dataclass
from decimal import Decimal

from .currency_payload import CurrencyPayload
from .fee import plus_fee
from .quantity_increment import (to_compatible_quantity_increment,
                                 validate_quantity_increments)
from .spread import get_spread


@dataclass(frozen=True)
class OrderData:
    """Has data of ready for arbitrage order.

    Args:
        price (Decimal): currency price.
        quantity (Decimal): currency quantity.
        estimated_value (Decimal): currency estimated value in quote currency.
    """

    price: Decimal
    quantity: Decimal
    estimated_value: Decimal


@dataclass(frozen=True)
class OrdersData:
    """Has data of ready for arbitrage bid and ask orders and spread, profit between them.

    Args:
        ask (OrderData): ask order data.
        bid (OrderData): bid order data.
        spread (OrderData): clear spread between ask and bid orders.
        profit (OrderData): clear profit between ask and bid orders.
    """

    ask: OrderData
    bid: OrderData
    spread: Decimal
    profit: Decimal


@dataclass(frozen=True)
class OrderPayload:
    """Has data from order from exchange: price, quantity, quantity_increment, fee.

    Args:
        price (Decimal): currency price.
        quantity (Decimal): currency quantity.
        quantity_increment (Decimal): currency quantity increment.
        fee (Decimal): currency fee.
        ask_fee_in_base_currency (bool): True if exchange takes fee in base currency.
    """

    price: Decimal
    quantity: Decimal
    quantity_increment: Decimal
    fee: Decimal
    ask_fee_in_base_currency: bool = False


def create_orders_data(*, ask_currency_payload: CurrencyPayload,
                       bid_currency_payload: CurrencyPayload,
                       make_compatible_quantity_increments: bool = True
                       ) -> OrdersData:
    """Creates ask and bid orders data.

    Calculates spread, profit between ask and bid orders.
    Selects min currency quantity from ask and bid orders.

    Args:
        ask_currency_payload (CurrencyPayload): ask currency payload.
        bid_currency_payload (CurrencyPayload): bid currency payload.
        make_compatible_quantity_increments (bool, optional): if True will be chosen 
            max quantity increment from ask and bid for ask and bid. Defaults to True.

    Returns:
        OrdersData
    """

    ask_price = ask_currency_payload.price
    bid_price = bid_currency_payload.price
    ask_cp_qty_inc = ask_currency_payload.quantity_increment
    bid_cp_qty_inc = bid_currency_payload.quantity_increment

    if make_compatible_quantity_increments:
        validate_quantity_increments(ask_cp_qty_inc, bid_cp_qty_inc)
        ask_qty_inc = bid_qty_inc = max(
            ask_cp_qty_inc, bid_cp_qty_inc)
    else:
        ask_qty_inc = ask_cp_qty_inc
        bid_qty_inc = bid_cp_qty_inc

    ask_quantity = bid_quantity = max(
        min(ask_currency_payload.quantity, bid_currency_payload.quantity),
        ask_currency_payload.min_quantity, bid_currency_payload.min_quantity)

    ask_order_payload = OrderPayload(
        ask_price, ask_quantity, ask_qty_inc, ask_currency_payload.fee,
        ask_currency_payload.ask_fee_in_base_currency)
    bid_order_payload = OrderPayload(
        bid_price, bid_quantity, bid_qty_inc, bid_currency_payload.fee,
        bid_currency_payload.ask_fee_in_base_currency)

    ask_order_data = create_ask_order_data(ask_order_payload)
    bid_order_data = create_bid_order_data(bid_order_payload)
    ask_estimated_value = ask_order_data.estimated_value
    bid_estimated_value = bid_order_data.estimated_value
    spread = get_spread(ask_estimated_value, bid_estimated_value)
    profit = bid_estimated_value - ask_estimated_value

    return OrdersData(ask=ask_order_data, bid=bid_order_data, spread=spread, profit=profit)


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

    if order_payload.ask_fee_in_base_currency:
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

    estimated_value = qty * price
    estimated_value -= estimated_value * fee / 100

    return OrderData(price=price, quantity=qty, estimated_value=estimated_value)
