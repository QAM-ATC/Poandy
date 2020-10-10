from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller


class PricingController(Controller):
    @classmethod
    def get_pricing(
        cls,
        account_id,
        instruments,
        since=None,
        includeUnitsAvailable=True,
        includeHomeConversions=False,
    ):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/pricing"
        response = RequestSender.send(
            url,
            cls._headers,
            RequestType.GET,
            params={
                "instruments": ",".join(instruments),
                "since": since,
                "includeUnitsAvailable": includeUnitsAvailable,
                "includeHomeConversions": includeHomeConversions,
            },
        )
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )

    @classmethod
    def get_latest_candles(
        cls,
        account_id,
        candleSpecifications,
        units=1,
        smooth=False,
        dailyAlignment=17,
        alignmentTimeZone="America/New_York",
        weeklyAlignment="Friday",
    ):
        url = f"{cls._config['base_url']}/v3/accounts/{account_id}/candles/latest"
        if dailyAlignment < 0 or dailyAlignment > 23:
            raise ValueError("dailyAlignment should be between 0 and 23 (inclusive)")

        response = RequestSender.send(
            url,
            cls._headers,
            RequestType.GET,
            params={
                "candleSpecifications": candleSpecifications,
                "units": units,
                "smooth": smooth,
                "dailyAlignment": dailyAlignment,
                "alignmentTimeZone": alignmentTimeZone,
                "weeklyAlignment": weeklyAlignment,
            },
        )
        return (
            response.json()
            if response.status_code == 200
            else response.raise_for_status()
        )
