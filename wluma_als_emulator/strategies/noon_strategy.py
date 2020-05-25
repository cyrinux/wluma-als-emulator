# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from ..helpers.solar_api import SolarApi


class NoonStrategy:
    def __init__(self, config):
        """
        Strategy with "midday" equal to the sun noon time.
        """
        self.config = config
        self.api = SolarApi(config)
        self.lux = None
        self.sleep_time = self.config.sleep_time

    def calculate(self):
        # refresh data api
        self.api.fetch()

        solar_noon = self.api.get("solar_noon")
        solar_noon_in_seconds = self.api.get("solar_noon_in_seconds")
        solar_noon_date = datetime.combine(datetime.now().date(), solar_noon.time())

        # get the time 12h before the noon
        now = datetime.now() - (solar_noon_date - timedelta(hours=12))
        now_in_seconds = now.seconds

        # from 12h before the noon to noon
        if now_in_seconds > solar_noon_in_seconds:
            lux = 100 - ((now_in_seconds * 100 / solar_noon_in_seconds) - 100)
        else:
            # after the noon to midnight
            lux = now_in_seconds * 100 / solar_noon_in_seconds

        if self.config.verbose:
            print(
                "lux={} | noon={} | waiting {} seconds...".format(
                    round(lux, 3), solar_noon_date, self.sleep_time
                )
            )
        return int(lux)

    def run(self):
        self.lux = self.calculate()
