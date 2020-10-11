from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller

import pandas as pd
from dateutil.parser import isoparse

class InstrumentController(Controller):
    @classmethod
    def get_candles(cls, instrument_name, candle_params={}, df=True):
        url = f"{cls._config['base_url']}/v3/instruments/{instrument_name}/candles"
        response = RequestSender.send(
            url, cls._headers, RequestType.GET, params=candle_params
        )

        if response.status_code == 200:
            candles = response.json()
            if not df:
                return candles
            candles["candles"] = pd.DataFrame(candles["candles"])
            candles["candles"]["time"] = pd.to_datetime(
                candles["candles"]["time"], unit="s"
            )
            for price in ["mid", "bid", "ask"]:
                if price not in candles["candles"].columns:
                    continue
                candles["candles"][f"{price}.open"] = (
                    candles["candles"][price].map(lambda x: x["o"]).astype(float)
                )
                candles["candles"][f"{price}.high"] = (
                    candles["candles"][price].map(lambda x: x["h"]).astype(float)
                )
                candles["candles"][f"{price}.low"] = (
                    candles["candles"][price].map(lambda x: x["l"]).astype(float)
                )
                candles["candles"][f"{price}.close"] = (
                    candles["candles"][price].map(lambda x: x["c"]).astype(float)
                )
                del candles["candles"][price]
            return candles["candles"]
        return response.raise_for_status()

    @classmethod
    def get_orderbook(cls, instrument_name, time=None, df=True):
        url = f"{cls._config['base_url']}/v3/instruments/{instrument_name}/orderBook"
        response = RequestSender.send(
            url, cls._headers, RequestType.GET, params={"time": time}
        )

        if response.status_code == 200:
            orderbook = response.json()["orderBook"]
            if not df:
                return orderbook
            # orderbook['time'] is UTC time, so it is consistent with the time given in the candles
            # there is also orderbook['unixTime'], but it seems like it's Singapore time UTC+8
            orderbook["time"] = isoparse(orderbook["time"][:-1])
            orderbook["price"] = float(orderbook["price"])
            orderbook["bucketWidth"] = float(orderbook["bucketWidth"])
            orderbook["buckets"] = pd.DataFrame(orderbook["buckets"]).astype(float)
            print(
                f"Time of order book: {orderbook['time'].strftime('%d/%m/%Y, %H:%M:%S')}"
            )
            print(f"Midpoint price: {orderbook['price']}")
            print(
                f"Bucket width: {orderbook['bucketWidth']}. Each bucket covers from bucket price to bucket price + bucket width"
            )
            return orderbook["buckets"]
        return response.raise_for_status()

    @classmethod
    def get_positionbook(cls, instrument_name, time=None, df=True):
        url = f"{cls._config['base_url']}/v3/instruments/{instrument_name}/positionBook"
        response = RequestSender.send(
            url, cls._headers, RequestType.GET, params={"time": time}
        )

        if response.status_code == 200:
            positionbook = response.json()["positionBook"]
            if not df:
                return positionbook
            positionbook["time"] = isoparse(positionbook["time"][:-1])
            positionbook["price"] = float(positionbook["price"])
            positionbook["bucketWidth"] = float(positionbook["bucketWidth"])
            positionbook["buckets"] = pd.DataFrame(positionbook["buckets"]).astype(
                float
            )
            print(
                f"Time of position book: {positionbook['time'].strftime('%d/%m/%Y, %H:%M:%S')}"
            )
            print(f"Midpoint price: {positionbook['price']}")
            print(
                f"Bucket width: {positionbook['bucketWidth']}. Each bucket covers from bucket price to bucket price + bucket width    "
            )
            return positionbook["buckets"]
        return response.raise_for_status()
