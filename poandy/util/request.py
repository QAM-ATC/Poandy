from enum import Enum, auto
import requests

from poandy.util.objectless import Objectless


class RequestType(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    STREAM = auto()


class RequestSender(Objectless):
    @staticmethod
    def send(endpoint, headers, method, params={}, data={}):
        if method == RequestType.GET:
            return requests.get(endpoint, headers=headers, params=params, json=data)
        elif method == RequestType.POST:
            return requests.post(endpoint, headers=headers, params=params, json=data)
        elif method == RequestType.PUT:
            return requests.put(endpoint, headers=headers, params=params, json=data)
        elif method == RequestType.STREAM:
            return requests.get(endpoint, headers=headers, params=params, json=data, stream=True)


class ParamsBuilder:
    def __init__(self):
        self._d = {}

    def add(self, key, value):
        # Builder pattern allows this usage: params = ParamsBuilder().add("k1" 1).add("k2", 2).build()
        if key in self._d:
            self._d[key].append(value)
        else:
            self._d[key] = value
        return self

    def build(self):
        return self._d
