# -*- coding: utf-8 -*-
from datetime import datetime

from ..helpers.solar_api import SolarApi


class DayLightStrategy:
    def __init__(self, config):
        """
        WIP: Improved NoonStrategy but with usage of day length, sunrise and sunset
        """
        self.config = config
        self.lux = None
        self.sleep_time = self.config.sleep_time
        self.api = SolarApi(config)

    def calculate(self):
        self.api.fetch()

        civil_twilight_begin_in_seconds = self.api.get(
            "civil_twilight_begin_in_seconds"
        )
        civil_twilight_end_in_seconds = self.api.get("civil_twilight_end_in_seconds")
        civil_twilight_end = self.api.get("civil_twilight_end")
        day_length_in_seconds = self.api.get("day_length_in_seconds")
        solar_noon_in_seconds = self.api.get("solar_noon_in_seconds")

        day_length_percent_duration = (day_length_in_seconds * 100) / 86400
        night_percent_duration = 100 - day_length_percent_duration
        print(
            "day: {}% night: {}%".format(
                int(day_length_percent_duration), int(night_percent_duration)
            )
        )
        datenow = datetime.now()
        midnight = datetime.combine(datenow.date(), civil_twilight_end.time())
        now = midnight - datenow
        now_in_seconds = now.seconds

        # from noon to sunset
        print(
            "now: {}, noon: {}, civil_twilight_begin: {}, civil_twilight_end: {}".format(
                now_in_seconds,
                solar_noon_in_seconds,
                civil_twilight_begin_in_seconds,
                civil_twilight_end_in_seconds,
            )
        )
        # print((now_in_seconds * 100) / day_length_in_seconds)
        if (
            now_in_seconds > civil_twilight_begin_in_seconds
            and now_in_seconds < civil_twilight_end_in_seconds
        ):
            print(
                "{} > {} and {} < {}".format(
                    now_in_seconds,
                    civil_twilight_begin_in_seconds,
                    now_in_seconds,
                    civil_twilight_end_in_seconds,
                )
            )
            lux = (now_in_seconds * 100) / day_length_in_seconds
        else:
            # night
            lux = 0

        if self.config.verbose:
            print(
                "lux={} | time={} | waiting {} seconds...".format(
                    int(lux), datetime.now(), self.sleep_time,
                )
            )

        return int(lux)

    def loop(self):
        self.lux = self.calculate()
