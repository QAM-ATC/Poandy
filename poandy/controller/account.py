from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller


class AccountController(Controller):
    @classmethod
    def get_accounts(cls):
        url = f"{cls._config['base_url']}/v3/accounts"
        response = RequestSender.send(url, cls._headers, RequestType.GET)

        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_default_account_id(cls):
        return cls.get_accounts()["accounts"][0]["id"]

    @classmethod
    def get_account_details(cls, account_id):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_account_summary(cls, account_id):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/summary"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_tradeable_instruments(cls, account_id, names_only=False, instruments=[]):
        if instruments and names_only:
            raise Exception("names_only must be False if instruments is not empty")
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/instruments"
        response = RequestSender.send(
            url, cls._headers, RequestType.GET, params={"instruments": instruments}
        )
        if response.status_code != 200:
            response.raise_for_status()
        if not names_only:
            return response.json()
        else:
            return [instrument["name"] for instrument in response.json()["instruments"]]

    @classmethod
    def get_account_changes(cls, account_id, since_transaction_id=None):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/changes"
        response = RequestSender.send(
            url,
            cls._headers,
            RequestType.GET,
            params={"sinceTransactionID": since_transaction_id},
        )
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
