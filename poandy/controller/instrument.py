from poandy.util.request import RequestSender, RequestType
from poandy.controller.base import Controller
from poandy.util.utils import Utils

import pandas as pd
from dateutil.parser import isoparse


class InstrumentController(Controller):
    @classmethod
    def get_historical(
        cls, instrument_name, start="2000-01-01 00:00:00", end="2020-10-01 00:00:00"
    ):
        # wrapper around get_candles, bypass the 5000 count limit
        start_timestamp = Utils.get_unix_timestamp(start)
        end_timestamp = Utils.get_unix_timestamp(end)
        if max(start_timestamp, end_timestamp) > Utils.get_unix_timestamp("NOW"):
            raise Exception("Time cannot be greater than current time")

        full_candles = []
        while True:
            try:
                candles = cls.get_candles(
                    instrument_name, candle_params={"from": start_timestamp}
                )
                if candles.iloc[-1]["unixtime"] >= end_timestamp:
                    full_candles.append(
                        candles.loc[candles["unixtime"] <= end_timestamp]
                    )
                    break
                else:
                    full_candles.append(candles)
                    start_timestamp = candles.iloc[-1]["unixtime"] + 5
                patience = 5
            except Exception as e:
                patience -= 1
                if patience == 0:
                    raise

        return pd.concat(full_candles)

    @classmethod
    def get_candles(cls, instrument_name, candle_params={}, df=True):
        url = f"{cls._config['base_url']}/v3/instruments/{instrument_name}/candles"
        default_params = {
            "granularity": "S5",
            "count": 5000,
        }
        for k, v in default_params.items():
            if k not in candle_params:
                candle_params[k] = v
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
            candles["candles"]["unixtime"] = (
                candles["candles"]["time"]
                .astype(str)
                .apply(lambda x: int(Utils.get_unix_timestamp(x)))
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
            return positionbook["buckets"]
        return response.raise_for_status()
