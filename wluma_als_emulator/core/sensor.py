# -*- coding: utf-8 -*-

import signal
import os.path
import os
from time import sleep
from pathlib import Path
import sys

LOCKFILE = "wluma-als-emulator.lock"


class Sensor:
    def __init__(self, strategy):
        self.config = strategy.config
        self.strategy = strategy
        self.create_fake_sensor()
        self.prev_lux = None
        self.lux = None

        # on exit do
        signal.signal(signal.SIGTERM, self.exit_handler)
        signal.signal(signal.SIGINT, self.exit_handler)

        # lock
        if os.path.isfile(self.lockfile()):
            print("{} is already running!".format(os.path.basename(__file__)))
            sys.exit(2)
        Path(self.lockfile()).touch()

    def run(self):
        """
        Start a loop with the choosen strategy
        """
        while True:
            self.strategy.loop()
            if self.strategy.lux != self.prev_lux:
                self.prev_lux = self.strategy.lux
                self.write_lux(self.strategy.lux)

            # wait
            sleep(self.config.sleep_time)

    def lockfile(self):
        return self.config.output_basedir + "/" + LOCKFILE

    def cleanup(self):
        os.remove(self.lockfile())

    def exit_handler(self, signal, _):
        print("Receive signal {}, shutdown ALS emulator...".format(signal))
        self.cleanup()
        sys.exit(0)

    def create_fake_sensor(self):
        """
        Initialize the "fake" sensor in the output dir
        """
        # create fake /sys dir
        Path(self.config.output_basedir).mkdir(parents=True, exist_ok=True)

        als_raw = self.config.output_basedir + "/in_illuminance_raw"
        als_name = self.config.output_basedir + "/name"

        if not os.path.isfile(als_name):
            name = open(als_name, "w")
            name.write("als")
            name.flush()

        if self.config.verbose:
            print("input: {}, output: {}".format(self.config.input, als_raw))

        self.sensor = open(als_raw, "w+")

    def write_lux(self, lux):
        """
        Write sensor value to a file
        """
        self.sensor.seek(0)
        self.sensor.truncate()
        self.sensor.write(str(lux))
        self.sensor.flush()
        os.fsync(self.sensor)
