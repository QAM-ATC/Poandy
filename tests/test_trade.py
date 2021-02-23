import pytest

from poandy.controller.trade import TradeController
from poandy.controller.order import OrderController
from poandy.controller.account import AccountController


class TestTradeController:
    account_id = AccountController.get_default_account_id()
    instrument = "USD_CAD"
    # NOTE: if there are errors in creating orders (e.g. insufficient funds), the tests will fail
    # NOTE: in some tests, if an assertions fails, the code to close position will not be executed

    def test_get_trades_default(self):
        # open position
        order = OrderController.create_order(
            self.account_id, "MARKET", "100", self.instrument, "FOK", "DEFAULT"
        )
        id = order["orderFillTransaction"]["tradeOpened"]["tradeID"]

        trades = TradeController.get_trades(self.account_id)
        assert isinstance(trades, dict)
        assert "trades" in trades
        assert "lastTransactionID" in trades
        assert isinstance(trades["trades"], list)
        assert trades["trades"][0]["id"] == id
        assert trades["trades"][0]["instrument"] == self.instrument

        # close position
        OrderController.create_order(
            self.account_id, "MARKET", "-100", "USD_CAD", "FOK", "DEFAULT"
        )

    def test_get_trades_with_params(self):
        state = "CLOSED"
        count = 10
        ids = []

        # create closed trades: buy then sell immediately
        for _ in range(count):
            order = OrderController.create_order(
                self.account_id, "MARKET", "100", self.instrument, "FOK", "DEFAULT"
            )
            ids.append(order["orderFillTransaction"]["tradeOpened"]["tradeID"])
        OrderController.create_order(
            self.account_id,
            "MARKET",
            str(-100 * count),
            self.instrument,
            "FOK",
            "DEFAULT",
        )

        trades = TradeController.get_trades(
            self.account_id,
            ids=ids,
            state=state,
            instrument=self.instrument,
            count=count,
        )
        assert len(trades["trades"]) == count
        for trade in trades["trades"]:
            assert trade["id"] in ids
            assert trade["state"] == state
            assert trade["instrument"] == self.instrument

        trades = TradeController.get_trades(
            self.account_id,
            ids=ids,
            state=state,
            instrument=self.instrument,
            beforeID=ids[-1],
        )
        assert len(trades["trades"]) == count - 1  # beforeID is not included

    def test_get_trades_with_invalid_params(self):
        state = "TEST"
        count = 600
        with pytest.raises(ValueError):
            TradeController.get_trades(self.account_id, state=state)
            TradeController.get_trades(self.account_id, count=count)

    def test_get_open_trades(self):
        count = 10
        ids = []
        for _ in range(count):
            order = OrderController.create_order(
                self.account_id, "MARKET", "100", self.instrument, "FOK", "DEFAULT"
            )
            ids.append(order["orderFillTransaction"]["tradeOpened"]["tradeID"])

        open_trades = TradeController.get_open_trades(self.account_id)
        assert isinstance(open_trades, dict)
        assert "trades" in open_trades
        assert "lastTransactionID" in open_trades
        assert isinstance(open_trades["trades"], list)
        assert len(open_trades["trades"]) >= count
        for trade in open_trades["trades"]:
            assert trade["id"] in ids

        # close position
        OrderController.create_order(
            self.account_id,
            "MARKET",
            str(-100 * count),
            self.instrument,
            "FOK",
            "DEFAULT",
        )

    # NOTE: there must not be any trades when executing this test
    def test_empty_get_open_trades(self):
        open_trades = TradeController.get_open_trades(self.account_id)
        assert len(open_trades["trades"]) == 0

    def test_get_specific_trade(self):
        # open position
        order = OrderController.create_order(
            self.account_id, "MARKET", "100", self.instrument, "FOK", "DEFAULT"
        )
        id = order["orderFillTransaction"]["tradeOpened"]["tradeID"]

        trade = TradeController.get_specific_trade(self.account_id, tradeSpecifier=id)
        assert trade["trade"]["id"] == id
        assert trade["trade"]["instrument"] == self.instrument

        # close position
        order = OrderController.create_order(
            self.account_id, "MARKET", "-100", self.instrument, "FOK", "DEFAULT"
        )
