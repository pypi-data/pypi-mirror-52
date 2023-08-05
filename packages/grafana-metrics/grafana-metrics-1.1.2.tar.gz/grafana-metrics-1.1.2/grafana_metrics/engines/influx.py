# coding: utf-8
from __future__ import unicode_literals

from .base import Engine


class InfluxDB(Engine):
    """
    Engine InfluxDB v0.9 and higher
    """

    def __init__(self, host, port, database, username=None, password=None):
        from influxdb import InfluxDBClient
        self.client = InfluxDBClient(
            host=host,
            port=port,
            timeout=10,
            database=database,
            username=username,
            password=password
        )

    def send(self, metrics):
        self.client.write_points([m.to_influx() for m in metrics])
        return True
