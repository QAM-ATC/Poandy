from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller


class TradeController(Controller):
    @classmethod
    def get_trades(
        cls,
        account_id,
        ids=None,
        state="OPEN",
        instrument=None,
        count=50,
        beforeID=None,
    ):
        if state not in ["OPEN", "CLOSED", "CLOSE_WHEN_TRADEABLE", "ALL"]:
            raise ValueError(
                "state must be a valid TradeStateFilter (OPEN, CLOSED, CLOSE_WHEN_TRADEABLE, or ALL)"
            )
        if count < 1 or count > 500:
            raise ValueError("count must be positive and not exceed 500")

        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/trades"
        params = {"state": state, "count": count}
        if ids:
            # required format is csv
            params["ids"] = ",".join(ids)
        if instrument:
            params["instrument"] = instrument
        if beforeID:
            params["beforeID"] = beforeID

        response = RequestSender.send(url, cls._headers, RequestType.GET, params=params)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_open_trades(cls, account_id):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/openTrades"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_specific_trade(cls, account_id, tradeSpecifier):
        # tradeSpecifier is either TradeID or @ClientID
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/trades/{tradeSpecifier}"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
