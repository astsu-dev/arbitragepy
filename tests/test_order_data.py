from decimal import Decimal

from arbitrageutils import (CurrencyPayload,
                            ImcompabileQuantityIncrementsError, OrderData,
                            OrderPayload, OrdersData, create_ask_order_data,
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
    assert not op.ask_fee_in_base_currency

    op = OrderPayload(price=Decimal("14.5"), quantity=Decimal("1200"), quantity_increment=Decimal(
        "20"), fee=Decimal("5"), ask_fee_in_base_currency=True)
    assert op.price == Decimal("14.5")
    assert op.quantity == Decimal("1200")
    assert op.quantity_increment == Decimal("20")
    assert op.fee == Decimal("5")
    assert op.ask_fee_in_base_currency


def test_create_ask_order_data() -> None:
    op = OrderPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"))
    od = create_ask_order_data(op)
    assert od.price == Decimal("14.5")
    assert od.quantity == Decimal("1180")
    assert od.estimated_value == Decimal("18010.52631578947368421052632")

    op = OrderPayload(price=Decimal("14.5"), quantity=Decimal("1199"), quantity_increment=Decimal(
        "20"), fee=Decimal("5"), ask_fee_in_base_currency=True)
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
    # Ask fee in quote currency
    ask_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"))
    bid_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("40"), fee=Decimal("5"))
    orders_data = create_orders_data(
        ask_currency_payload=ask_cp, bid_currency_payload=bid_cp)
    assert orders_data.ask == OrderData(price=Decimal("14.5"), quantity=Decimal(
        "1160"), estimated_value=Decimal("17705.26315789473684210526316"))
    assert orders_data.bid == OrderData(price=Decimal(
        "14.5"), quantity=Decimal("1160"), estimated_value=Decimal("15979"))
    assert orders_data.spread == Decimal("-9.75000000000000000000000001")
    assert orders_data.profit == Decimal("-1726.26315789473684210526316")

    # Ask fee in base currency
    ask_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"), ask_fee_in_base_currency=True)
    bid_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("40"), fee=Decimal("5"))
    orders_data = create_orders_data(
        ask_currency_payload=ask_cp, bid_currency_payload=bid_cp)
    assert orders_data.ask == OrderData(price=Decimal("14.5"), quantity=Decimal(
        "1200"), estimated_value=Decimal("17400"))
    assert orders_data.bid == OrderData(price=Decimal(
        "14.5"), quantity=Decimal("1160"), estimated_value=Decimal("15979"))
    assert orders_data.spread == Decimal("-8.166666666666666666666666670")
    assert orders_data.profit == Decimal("-1421")

    # Not make compatible quantity increments
    ask_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"))
    bid_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("40"), fee=Decimal("5"))
    orders_data = create_orders_data(
        ask_currency_payload=ask_cp, bid_currency_payload=bid_cp, make_compatible_quantity_increments=False)
    assert orders_data.ask == OrderData(price=Decimal("14.5"), quantity=Decimal(
        "1180"), estimated_value=Decimal("18010.52631578947368421052632"))
    assert orders_data.bid == OrderData(price=Decimal(
        "14.5"), quantity=Decimal("1160"), estimated_value=Decimal("15979"))
    assert orders_data.spread == Decimal("-11.27966101694915254237288138")
    assert orders_data.profit == Decimal("-2031.52631578947368421052632")

    ask_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("15"), fee=Decimal("5"))
    bid_cp = CurrencyPayload(price=Decimal("14.5"), quantity=Decimal(
        "1199"), quantity_increment=Decimal("20"), fee=Decimal("5"))

    try:
        create_orders_data(ask_currency_payload=ask_cp,
                           bid_currency_payload=bid_cp)
    except ImcompabileQuantityIncrementsError:
        ...
    else:
        assert False
