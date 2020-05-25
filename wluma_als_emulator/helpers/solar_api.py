# -*- coding: utf-8 -*-

import pprint
from datetime import datetime
import json
import requests

API_URL = "https://api.sunrise-sunset.org/json"


class SolarApi:
    def __init__(self, config):
        self.config = config
        self.previous_day = None
        self.data = None

    def fetch(self):
        """
        Get data from the api plus some converted data
        """
        current_day = datetime.now().date()
        if self.previous_day != current_day:
            try:
                self.data = self.get_json()
                if self.config.verbose:
                    pprint.pprint(self.data)
                self.previous_day = current_day
            except:
                pass

        return self.convert_data(self.data)

    def time_to_localtime(self, data):
        """
        Convert from a time UTC to a datetime in locale TZ a format like "08:42:01 PM"
        """
        return datetime.combine(
            datetime.now().date(),
            datetime.strptime(data, "%I:%M:%S %p")
            .replace(tzinfo=self.config.from_zone)
            .astimezone(self.config.to_zone)
            .time(),
        )

    def time_in_seconds(self, data):
        """
        Convert a datetime to seconds since the start of the day
        """
        return (data.hour * 60 * 60) + (data.minute * 60) + data.second

    def get(self, key):
        return self.data["converted"][key]

    def convert_data(self, data):
        """
        Extend api data with some needed converted data
        """
        civil_twilight_begin = self.time_to_localtime(
            data["results"]["civil_twilight_begin"]
        )
        civil_twilight_begin_in_seconds = self.time_in_seconds(civil_twilight_begin)
        civil_twilight_end = self.time_to_localtime(
            data["results"]["civil_twilight_end"]
        )
        civil_twilight_end_in_seconds = self.time_in_seconds(civil_twilight_end)
        day_length = datetime.strptime(data["results"]["day_length"], "%H:%M:%S")
        day_length_in_seconds = self.time_in_seconds(day_length)
        solar_noon = self.time_to_localtime(data["results"]["solar_noon"])
        solar_noon_in_seconds = self.time_in_seconds(solar_noon)
        solar_sunrise = self.time_to_localtime(data["results"]["sunrise"])
        solar_sunrise_in_seconds = self.time_in_seconds(solar_sunrise)
        solar_sunset = self.time_to_localtime(data["results"]["sunset"])
        solar_sunset_in_seconds = self.time_in_seconds(solar_sunset)
        convertion = {
            "civil_twilight_begin": civil_twilight_begin,
            "civil_twilight_begin_in_seconds": civil_twilight_begin_in_seconds,
            "civil_twilight_end": civil_twilight_end,
            "civil_twilight_end_in_seconds": civil_twilight_end_in_seconds,
            "day_length": day_length,
            "day_length_in_seconds": day_length_in_seconds,
            "solar_noon_in_seconds": solar_noon_in_seconds,
            "solar_noon": solar_noon,
            "solar_sunrise_in_seconds": solar_sunrise_in_seconds,
            "solar_sunrise": solar_sunrise,
            "solar_sunset_in_seconds": solar_sunset_in_seconds,
        }

        self.data["converted"] = convertion

        return self.data

    def get_json(self):
        url = "{}?lat={}&lng={}&date=today&formatted=1".format(
            API_URL, self.config.gps["latitude"], self.config.gps["longitude"]
        )

        r = requests.get(url)
        if r.status_code != 200:
            print(
                "Can't get api results from: {}, status code {}".format(
                    url, r.status_code
                )
            )
            return self.data
        return json.loads(r.text)
