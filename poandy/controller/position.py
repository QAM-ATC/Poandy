from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller


class PositionController(Controller):
    @classmethod
    def get_positions(cls, account_id):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/positions"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_open_positions(cls, account_id):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/openPositions"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_instrument_positions(cls, account_id, instrument):
        url = (
            f"{cls._config['base_url']}/v3/accounts/{account_id}/positions/{instrument}"
        )
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def close_instrument_positions(
        cls, account_id, instrument, long_units=0, short_units=0
    ):
        if long_units != 0 and short_units != 0:
            raise Exception("Only long_units or short_units")
        elif long_units and short_units:
            raise Exception("No units specified")

        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/positions/{instrument}/close"
        data = (
            {"shortUnits": str(short_units)}
            if short_units
            else {"longUnits": str(long_units)}
        )
        response = RequestSender.send(url, cls._headers, RequestType.PUT, data=data)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
