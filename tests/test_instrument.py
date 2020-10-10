import pytest
import pandas as pd

from poandy.controller.instrument import InstrumentController


class TestInstrumentController:
    def test_get_candles(self):
        candles = InstrumentController.get_candles('USD_CAD')
        assert isinstance(candles, pd.DataFrame)

    def test_get_candles_raw(self):
        candles = InstrumentController.get_candles('USD_CAD', df=False)
        assert isinstance(candles, dict)
        assert 'instrument' in candles
        assert 'granularity' in candles
        assert 'candles' in candles
        
    def test_get_orderbook(self):
        orderbook = InstrumentController.get_orderbook('USD_CAD')
        assert isinstance(orderbook, pd.DataFrame)

    def test_get_orderbook_raw(self):
        orderbook = InstrumentController.get_orderbook('USD_CAD', df=False)
        assert isinstance(orderbook, dict)
        assert 'instrument' in orderbook
        assert 'time' in orderbook
        assert 'price' in orderbook
        assert 'bucketWidth' in orderbook
        assert 'buckets' in orderbook

    def test_get_positionbook(self):
        positionbook = InstrumentController.get_positionbook('USD_CAD')
        assert isinstance(positionbook, pd.DataFrame)

    def test_get_positionbook_raw(self):
        positionbook = InstrumentController.get_positionbook('USD_CAD', df=False)
        assert isinstance(positionbook, dict)
        assert 'instrument' in positionbook
        assert 'time' in positionbook
        assert 'price' in positionbook
        assert 'bucketWidth' in positionbook
        assert 'buckets' in positionbook