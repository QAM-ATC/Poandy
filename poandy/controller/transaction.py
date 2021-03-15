from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller


class TransactionController(Controller):
    @classmethod
    def validate_filter_types(cls, filter_types):
        for ftype in filter_types:
                if (ftype not in cls._config['transaction_filters']):
                    raise ValueError("filter_types must contain valid filters as defined in TransactionsController.filters")

    @classmethod
    def get_transactions(cls, account_id, start_time = None, end_time = None, pageSize = 100, filter_types = None):
        if pageSize < 1 or pageSize > 1000:
            raise ValueError("pageSize must be positive and not exceed 1000")

        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/transactions"
        params = {"pageSize": pageSize}
        if start_time:
            params["from"] = start_time
        if end_time:
            params["to"] = end_time
        if filter_types and cls.validate_filter_types(filter_types):
                params["type"] = ",".join(filter_types)
        
        response = RequestSender.send(url, cls._headers, RequestType.GET, params=params)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_transaction(cls, account_id, transaction_id):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/transactions/{transaction_id}"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
    
    @classmethod
    def get_transactions_in_id_range(cls, account_id, from_id, to_id, filter_types = None):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/transactions/idrange"
        params = {"from": from_id, "to": to_id}

        if filter_types and cls.validate_filter_types(filter_types):
            params["type"] = ",".join(filter_types)

        response = RequestSender.send(url, cls._headers, RequestType.GET, params=params)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
    
    @classmethod
    def get_transactions_since_id(cls, account_id, start_id, filter_types = None):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/transactions/sinceid"
        params = {"id": start_id}

        if filter_types and cls.validate_filter_types(filter_types):
            params["type"] = ",".join(filter_types)

        response = RequestSender.send(url, cls._headers, RequestType.GET, params=params)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
    
    @classmethod
    def stream_transactions(cls, account_id):
        url = f"{cls._config['streaming_url']}/v3/accounts/{account_id}/transactions/stream"
        stream_response = RequestSender.send(url, cls._headers, RequestType.STREAM)

        return (
            stream_response
            if stream_response.status_code == 200
            else stream_response.raise_for_status()
        )

