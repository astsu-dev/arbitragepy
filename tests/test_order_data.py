from decimal import Decimal

from arbitrageutils import (CurrencyPayload, OrderData, OrderPayload,
                            OrdersData, create_ask_order_data,
                            create_bid_order_data, create_orders_data)


def test_order_data() -> None:
    od = OrderData(price=Decimal("14.5"), quantity=Decimal(
        "1200"), estimated_value=Decimal("342.423"))
    assert od.price == Decimal("14.5")
    assert od.quantity == Decimal("1200")
    assert od.estimated_value == Decimal("342.423")


def test_orders_data() -> None:
    od = OrderData(price=Decimal("14.5"), quantity=Decimal(
        "1200"), estimated_value=Decimal("342.423"))
    osd = OrdersData(ask=od, bid=od, spread=Decimal(
        "5.4"), profit=Decimal("500"))
    assert osd.ask == od
    assert osd.bid == od
    assert osd.spread == Decimal("5.4")
    assert osd.profit == Decimal("500")


def test_order_payload() -> None:
    op = OrderPayload(price=Decimal("14.5"), quantity=Decimal(
        "1200"), quantity_increment=Decimal("20"), fee=Decimal("5"))
    assert op.price == Decimal("14.5")
    assert op.quantity == Decimal("1200")
    assert op.quantity_increment == Decimal("20")
    assert op.fee == Decimal("5")
    assert not op.ask_fee_in_current_currency

    op = OrderPayload(price=Decimal("14.5"), quantity=Decimal("1200"), quantity_increment=Decimal(
        "20"), fee=Decimal("5"), ask_fee_in_current_currency=True)
    assert op.price == Decimal("14.5")
    assert op.quantity == Decimal("1200")
    assert op.quantity_increment == Decimal("20")
    assert op.fee == Decimal("5")
    assert op.ask_fee_in_current_currency


def test_create_ask_order_data() -> None:
    op = OrderPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"))
    od = create_ask_order_data(op)
    assert od.price == Decimal("14.5")
    assert od.quantity == Decimal("1180")
    assert od.estimated_value == Decimal("18010.52631578947368421052632")

    op = OrderPayload(price=Decimal("14.5"), quantity=Decimal("1199"), quantity_increment=Decimal(
        "20"), fee=Decimal("5"), ask_fee_in_current_currency=True)
    od = create_ask_order_data(op)
    assert od.price == Decimal("14.5")
    assert od.quantity == Decimal("1240")
    assert od.estimated_value == Decimal("17980")


def test_create_bid_order_data() -> None:
    op = OrderPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"))
    od = create_bid_order_data(op)
    assert od.price == Decimal("14.5")
    assert od.quantity == Decimal("1180")
    assert od.estimated_value == Decimal("16254.5")


def test_create_orders_data() -> None:
    ask_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"))
    bid_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"))
    orders_data = create_orders_data(
        ask_currency_payload=ask_cp, bid_currency_payload=bid_cp)
    assert orders_data.ask == OrderData(price=Decimal("14.5"), quantity=Decimal(
        "1180"), estimated_value=Decimal("18010.52631578947368421052632"))
    assert orders_data.bid == OrderData(price=Decimal(
        "14.5"), quantity=Decimal("1180"), estimated_value=Decimal("16254.5"))
    assert orders_data.spread == Decimal("0")
    assert orders_data.profit == Decimal(
        "16254.5") - Decimal("18010.52631578947368421052632")
