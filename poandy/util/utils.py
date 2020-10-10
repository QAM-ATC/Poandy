import json
import datetime

from poandy.util.objectless import Objectless


class Utils(Objectless):
    _config = None

    @classmethod
    def _load_config(cls):
        with open("config.json") as f:
            cls._config = json.load(f)
        with open(cls._config["secrets_path"]) as f:
            secrets = json.load(f)
        cls._config.update(secrets)

    @classmethod
    def get_config(cls):
        if not cls._config:
            cls._load_config()
        return cls._config

    @classmethod
    def get_authorization(cls):
        token = cls.get_config()["token"]
        return {"Authorization": f"Bearer {token}"}

    @classmethod
    def get_accept_datetime_format(cls):
        return {"Accept-Datetime-Format": "UNIX"}

    @classmethod
    def get_headers(cls):
        headers = {}
        headers.update(cls.get_authorization())
        headers.update(cls.get_accept_datetime_format())
        return headers

    @classmethod
    def get_unix_timestamp(cls):
        return datetime.datetime.now(datetime.timezone.utc).timestamp()

    @classmethod
    def get_ISO_datetime(cls, timestamp):
        return datetime.datetime.fromtimestamp(
            timestamp, datetime.timezone.utc
        ).isoformat()
