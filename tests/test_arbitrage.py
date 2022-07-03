from decimal import Decimal

import pytest

from arbitragepy.arbitrage import arbitrage
from arbitragepy.enums import OrderSide
from arbitragepy.exceptions import (
    ImcompabileQuantityIncrementsError,
    NotionalLessThanMinNotionalError,
    QuantityLessThanMinQuantityError,
)
from arbitragepy.models import (
    ArbitragePayload,
    ArbitrageResult,
    OrderInfo,
    OrderPayload,
    SymbolInfo,
)


def test_arbitrage() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.67815"),
            taken_fee=Decimal("0.52815"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("577.87155"),
            taken_fee=Decimal("0.57845"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.304980733552162123590695000"),
        profit=Decimal("49.1934"),
    )

    assert result == expected


def test_arbitrage_with_ask_fee_in_base_currency() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Ask fee in base currency.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
            fee_in_base_currency=True,
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.15"),
            taken_fee=Decimal("0.0503"),
            fee_in_base_currency=True,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.24"),
            notional_value=Decimal("577.18224"),
            taken_fee=Decimal("0.57776"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.283771655779608065890372100"),
        profit=Decimal("49.03224"),
    )

    assert result == expected


def test_arbitrage_when_bid_quantity_great_than_ask_quantity() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity great than ask order quantity.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.67815"),
            taken_fee=Decimal("0.52815"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("577.87155"),
            taken_fee=Decimal("0.57845"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.304980733552162123590695000"),
        profit=Decimal("49.1934"),
    )

    assert result == expected


def test_arbitrage_when_bid_quantity_great_than_ask_quantity_and_ask_fee_in_base_currency() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity great than ask order quantity.
    Ask fee in base currency.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
            fee_in_base_currency=True,
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.15"),
            taken_fee=Decimal("0.0503"),
            fee_in_base_currency=True,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.24"),
            notional_value=Decimal("577.18224"),
            taken_fee=Decimal("0.57776"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.283771655779608065890372100"),
        profit=Decimal("49.03224"),
    )

    assert result == expected


def test_arbitrage_with_ask_balance_less_than_order_quantity() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Ask balance less than bid balance and less than order quantity.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        balance=Decimal("200"),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        balance=Decimal("65"),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("19.02"),
            notional_value=Decimal("199.90971"),
            taken_fee=Decimal("0.19971"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("19.02"),
            notional_value=Decimal("218.51127"),
            taken_fee=Decimal("0.21873"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.304980733552162123590695000"),
        profit=Decimal("18.60156"),
    )

    assert result == expected


def test_arbitrage_with_ask_balance_less_than_order_quantity_and_ask_fee_in_base_currency() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Ask balance less than bid balance and less than order quantity.
    Ask fee in base currency.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
            fee_in_base_currency=True,
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        balance=Decimal("200"),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        balance=Decimal("65"),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("19.04"),
            notional_value=Decimal("199.92"),
            taken_fee=Decimal("0.01904"),
            fee_in_base_currency=True,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("19.02"),
            notional_value=Decimal("218.51127"),
            taken_fee=Decimal("0.21873"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.299354741896758703481392600"),
        profit=Decimal("18.59127"),
    )

    assert result == expected


def test_arbitrage_with_balances_great_than_order_quantity() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Balances great than order quantity.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        balance=Decimal("2000"),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        balance=Decimal("650"),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.67815"),
            taken_fee=Decimal("0.52815"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("577.87155"),
            taken_fee=Decimal("0.57845"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.304980733552162123590695000"),
        profit=Decimal("49.1934"),
    )

    assert result == expected


def test_arbitrage_with_balances_great_than_order_quantity_and_ask_fee_in_base_currency() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Balances great than order quantity.
    Ask fee in base currency.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
            fee_in_base_currency=True,
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        balance=Decimal("2000"),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        balance=Decimal("650"),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.15"),
            taken_fee=Decimal("0.0503"),
            fee_in_base_currency=True,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.24"),
            notional_value=Decimal("577.18224"),
            taken_fee=Decimal("0.57776"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.283771655779608065890372100"),
        profit=Decimal("49.03224"),
    )

    assert result == expected


def test_arbitrage_with_different_quantity_increments() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Different and compatible quantity increments.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.1")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.35")),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.67815"),
            taken_fee=Decimal("0.52815"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("577.87155"),
            taken_fee=Decimal("0.57845"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.304980733552162123590695000"),
        profit=Decimal("49.1934"),
    )

    assert result == expected


def test_arbitrage_dont_make_compatible_quantity_increments() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Different and imcompatible quantity increments. Does not make compatible.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.03")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.1")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )

    result = arbitrage(ask=ask, bid=bid, make_compatible_quantity_increments=False)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.28"),
            notional_value=Decimal("528.46794"),
            taken_fee=Decimal("0.52794"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("577.87155"),
            taken_fee=Decimal("0.57845"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.348459246174895680521319800"),
        profit=Decimal("49.40361"),
    )

    assert result == expected


def test_arbitrage_make_compatible_quantity_increments_with_imcompatible_increments() -> None:
    """Should raise `ImcompatibleQuantityIncrementsError`.
    Bid order quantity less than ask order quantity.
    Different and imcompatible quantity increments. Make compatible.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.03")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.1")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )

    with pytest.raises(ImcompabileQuantityIncrementsError):
        arbitrage(ask=ask, bid=bid)


def test_arbitrage_when_ask_quantity_less_than_min_quantity() -> None:
    """Should raise `QuantityLessThanMinQuantityError` exception.
    Ask quantity less than ask min quantity.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
            min_quantity=Decimal("100"),
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )

    with pytest.raises(QuantityLessThanMinQuantityError) as exc_info:
        arbitrage(ask=ask, bid=bid)

    exc = exc_info.value
    assert exc.side is OrderSide.ASK
    assert exc.quantity == Decimal("50.3")
    assert exc.min_quantity == Decimal("100")


def test_arbitrage_when_bid_quantity_less_than_min_quantity() -> None:
    """Should raise `QuantityLessThanMinQuantityError` exception.
    Bid quantity less than bid min quantity.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
            min_quantity=Decimal("100"),
        ),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )

    with pytest.raises(QuantityLessThanMinQuantityError) as exc_info:
        arbitrage(ask=ask, bid=bid)

    exc = exc_info.value
    assert exc.side is OrderSide.BID
    assert exc.quantity == Decimal("50.3")
    assert exc.min_quantity == Decimal("100")


def test_arbitrage_when_ask_notional_less_than_min_notional() -> None:
    """Should raise `NotionalLessThanMinNotionalError` exception.
    Ask notional value less than ask min notional value.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
            min_notional=Decimal("10000"),
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )

    with pytest.raises(NotionalLessThanMinNotionalError) as exc_info:
        arbitrage(ask=ask, bid=bid)

    exc = exc_info.value
    assert exc.side is OrderSide.ASK
    assert exc.notional == Decimal("528.67815")
    assert exc.min_notional == Decimal("10000")


def test_arbitrage_when_bid_notional_less_than_min_notional() -> None:
    """Should raise `NotionalLessThanMinNotionalError` exception.
    Bid notional value less than bid min notional value.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
        fee=Decimal("0.1"),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"),
            min_notional=Decimal("10000"),
        ),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
        fee=Decimal("0.1"),
    )

    with pytest.raises(NotionalLessThanMinNotionalError) as exc_info:
        arbitrage(ask=ask, bid=bid)

    exc = exc_info.value
    assert exc.side is OrderSide.BID
    assert exc.notional == Decimal("577.87155")
    assert exc.min_notional == Decimal("10000")


def test_arbitrage_with_zero_fee() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Ask and bid fee is 0.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("50.3")),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.15"),
            taken_fee=Decimal("0"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("578.45"),
            taken_fee=Decimal("0"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.523809523809523809523809500"),
        profit=Decimal("50.3"),
    )

    assert result == expected


def test_arbitrage_with_ask_max_quantity() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Ask and bid fee is 0.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"), max_quantity=Decimal("50.3")
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("60.3")),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.15"),
            taken_fee=Decimal("0"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("578.45"),
            taken_fee=Decimal("0"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.523809523809523809523809500"),
        profit=Decimal("50.3"),
    )

    assert result == expected


def test_arbitrage_with_bid_max_quantity() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Ask and bid fee is 0.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(quantity_increment=Decimal("0.01")),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"), max_quantity=Decimal("50.3")
        ),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("60.3")),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.15"),
            taken_fee=Decimal("0"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("578.45"),
            taken_fee=Decimal("0"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.523809523809523809523809500"),
        profit=Decimal("50.3"),
    )

    assert result == expected


def test_arbitrage_with_ask_and_bid_max_quantity() -> None:
    """Should correct arbitrage with the following conditions:
    Bid order quantity less than ask order quantity.
    Ask and bid fee is 0.
    """

    ask = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"), max_quantity=Decimal("50.3")
        ),
        order=OrderInfo(price=Decimal("10.5"), quantity=Decimal("100.15")),
    )
    bid = ArbitragePayload(
        symbol=SymbolInfo(
            quantity_increment=Decimal("0.01"), max_quantity=Decimal("52.3")
        ),
        order=OrderInfo(price=Decimal("11.5"), quantity=Decimal("60.3")),
    )

    result = arbitrage(ask=ask, bid=bid)
    expected = ArbitrageResult(
        ask_order=OrderPayload(
            price=Decimal("10.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("528.15"),
            taken_fee=Decimal("0"),
            fee_in_base_currency=False,
        ),
        bid_order=OrderPayload(
            price=Decimal("11.5"),
            quantity=Decimal("50.3"),
            notional_value=Decimal("578.45"),
            taken_fee=Decimal("0"),
            fee_in_base_currency=False,
        ),
        spread=Decimal("9.523809523809523809523809500"),
        profit=Decimal("50.3"),
    )

    assert result == expected
