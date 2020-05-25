# -*- coding: utf-8 -*-
import getopt
import os
import os.path
import sys
from dateutil import tz
from datetime import datetime

VERSION = "1.1.0"
FAKE_SENSOR = "/tmp/fake-devices"
INPUT = "/dev/video0"
DEFAULT_SLEEP_MODE = "lux"
DEFAULT_SLEEP_TIME = 30
DEFAULT_STRATEGY = "webcam"
GPS = {"latitude": "48.8566969", "longitude": "2.3514616"}


WEBCAM_SLEEP_PER_PERIODS = {
    300: [[0, 6], [20, 23]],
    15: [[6, 19]],
}


class Config:
    def __init__(self):
        # test params
        try:
            opts, _ = getopt.getopt(
                sys.argv[1:],
                "i:o:s:t:hvV",
                [
                    "input=",
                    "output=",
                    "sleep=",
                    "strategy=",
                    "help",
                    "verbose",
                    "version",
                ],
            )
        except getopt.GetoptError as err:
            print(err)
            self.usage()
            sys.exit(2)

        # default values
        self.from_zone = tz.tzutc()
        self.to_zone = tz.tzlocal()
        self.input = INPUT
        self.gps = GPS
        self.sleep_mode = DEFAULT_SLEEP_MODE
        self.sleep_time = DEFAULT_SLEEP_TIME
        self.strategy = DEFAULT_STRATEGY
        self.verbose = False
        self.output_basedir = (
            os.environ.get("WLUMA_AMBIENT_LIGHT_SENSOR_BASE_PATH", FAKE_SENSOR)
            + "/light-sensor"
        )
        self.strategy = os.environ.get(
            "WLUMA_AMBIENT_LIGHT_SENSOR_EMULATOR_STRATEGY", DEFAULT_STRATEGY
        )

        # get params values
        for opt, arg in opts:
            if opt in ("-v", "--verbose"):
                self.verbose = True
            elif opt in ("-i", "--input"):
                self.input = arg
            elif opt in ("-t", "--strategy"):
                self.strategy = arg
            elif opt in ("-s", "--sleep"):
                self.get_sleep_params(arg)
            elif opt in ("-o", "--output"):
                self.output_basedir = arg
            elif opt in ("-h", "--help"):
                self.usage()
                sys.exit(0)
            elif opt in ("-V", "--version"):
                print("version {}".format(VERSION))
                sys.exit(0)
            else:
                assert False, "unhandled option, see --help"

            if self.strategy != "webcam":
                self.input = "time based"

    def get_sleep_params(self, arg):
        if arg == "periods":
            self.sleep_mode = "periods"
        elif arg == "lux":
            self.sleep_mode = "lux"
        else:
            try:
                self.sleep_time = int(arg)
                self.sleep_mode = "fixed"
            except:
                self.sleep_time = int(DEFAULT_SLEEP_TIME)
                print(
                    "sleep must be an int or 'lux' or 'periods', default to {} seconds.".format(
                        DEFAULT_SLEEP_TIME
                    )
                )

    def get_sleep_by_periods(self):
        hour = datetime.now().hour
        sleep_time = 30
        for p in WEBCAM_SLEEP_PER_PERIODS:
            for r in WEBCAM_SLEEP_PER_PERIODS[p]:
                if hour in range(r[0], r[1]):
                    sleep_time = p
                    break
        return int(sleep_time)

    def usage(self):
        print(
            """{} [--input=/dev/video0] [--output=/tmp/fake-devicse]
               [--sleep=10/periods] [--strategy=webcam/time/noon/daylight] [--verbose] [--version]\n""".format(
                os.path.basename(__file__)
            )
        )

        print(
            "env WLUMA_AMBIENT_LIGHT_SENSOR_EMULATOR_STRATEGY can be use for 'strategy'"
        )
        print(
            "env WLUMA_AMBIENT_LIGHT_SENSOR_BASE_PATH if set will be use as output to play with wluma"
        )
