import pytest

from poandy.controller.pricing import PricingController
from poandy.controller.account import AccountController


class TestPricingController:
    def test_get_pricing(self):
        account_id = AccountController.get_default_account_id()
        assert isinstance(account_id, str)
        pricing = PricingController.get_pricing(account_id, ["EUR_USD", "USD_CAD"])
        assert isinstance(pricing, dict)
        assert "prices" in pricing

    def test_get_latest_candles_value_error(self):
        account_id = AccountController.get_default_account_id()
        with pytest.raises(ValueError):
            PricingController.get_latest_candles(
                account_id, ["EUR_USD:S10:BM"], dailyAlignment=25
            )

    def test_get_latest_candles(self):
        account_id = AccountController.get_default_account_id()
        latest_candles = PricingController.get_latest_candles(
            account_id, ["EUR_USD:S10:BM"]
        )

        assert isinstance(latest_candles, dict)
        assert "latestCandles" in latest_candles
