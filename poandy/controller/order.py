from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller


# TODO: Only support market order
class OrderController(Controller):
    @classmethod
    # TODO: Figure out which params are unnecessary and can be moved into other_params
    # TODO: Figure out which terms mean what
    def create_order(
        cls,
        account_id,
        order_type,
        units,
        instrument,
        time_in_force,
        position_fill,
        other_params={},
    ):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/orders"
        data = {
            "order": {
                "units": units,
                "instrument": instrument,
                "timeInForce": time_in_force,
                "type": order_type,
                "positionFill": position_fill,
            }
        }
        data["order"].update(other_params)
        response = RequestSender.send(url, cls._headers, RequestType.POST, data=data)
        return (
            response.json()
            if response.status_code == 201
            else response.raise_for_status()
        )

    @classmethod
    def get_orders(cls, account_id):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/orders"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_pending_orders(cls, account_id):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/pendingOrders"
        response = RequestSender.send(url, cls._headers, RequestType.GET)
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
