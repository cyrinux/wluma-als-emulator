from datetime import datetime, time

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
        # refresh data api
        self.api.fetch()

        civil_twilight_begin_in_seconds = self.api.get(
            "civil_twilight_begin_in_seconds"
        )
        civil_twilight_end_in_seconds = self.api.get("civil_twilight_end_in_seconds")
        civil_twilight_end = self.api.get("civil_twilight_end")
        civil_twilight_begin = self.api.get("civil_twilight_begin")
        day_length_in_seconds = self.api.get("day_length_in_seconds")

        day_length_percent_duration = (day_length_in_seconds * 100) / 86400
        night_percent_duration = 100 - day_length_percent_duration
        if self.config.verbose:
            print(
                "day length: {}% and night length: {}%".format(
                    int(day_length_percent_duration), int(night_percent_duration)
                )
            )
        datenow = (
            datetime.now()
            .replace(tzinfo=self.config.to_zone)
            .astimezone(self.config.to_zone)
        )
        midnight = (
            datetime.combine(datenow.date(), time(0))
            .replace(tzinfo=self.config.from_zone)
            .astimezone(self.config.to_zone)
        )

        now = midnight - datenow
        now_in_seconds = now.seconds

        if self.config.verbose:
            c1 = ">" if now_in_seconds > civil_twilight_begin_in_seconds else ">"
            c2 = "<" if now_in_seconds < civil_twilight_end_in_seconds else "<"
            print(
                "now: {} {} twilight_begin: {} and now: {} {} twilight_end: {}".format(
                    now_in_seconds,
                    c1,
                    civil_twilight_begin_in_seconds,
                    now_in_seconds,
                    c2,
                    civil_twilight_end_in_seconds,
                )
            )
        if (
            now_in_seconds > civil_twilight_begin_in_seconds
            and now_in_seconds < civil_twilight_end_in_seconds
        ):
            lux = (now_in_seconds * 100) / (
                civil_twilight_end - civil_twilight_begin
            ).total_seconds()
        else:
            lux = 0

        if self.config.verbose:
            print(
                "lux={} | time={} | twilight_begin={} | civil_twilight_end={} | waiting {} seconds...".format(
                    round(lux, 3),
                    datetime.now(),
                    civil_twilight_begin,
                    civil_twilight_end,
                    self.sleep_time,
                )
            )

        return int(lux)

    def run(self):
        self.lux = self.calculate()
