from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller


class InstrumentController(Controller):
    @classmethod
    def get_candles(cls, instrument_name, candle_params={}):
        url = f"{cls._config['base_url']}/v3/instruments/{instrument_name}/candles"
        response = RequestSender.send(
            url, cls._headers, RequestType.GET, params=candle_params
        )
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_orderbook(cls, instrument_name, datetime=None):
        url = f"{cls._config['base_url']}/v3/instruments/{instrument_name}/orderBook"
        response = RequestSender.send(
            url, cls._headers, RequestType.GET, params={"time": datetime}
        )
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_positionbook(cls, instrument_name, datetime=None):
        url = f"{cls._config['base_url']}/v3/instruments/{instrument_name}/positionBook"
        response = RequestSender.send(
            url, cls._headers, RequestType.GET, params={"time": datetime}
        )
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
