# -*- coding: utf-8 -*-

import math
import os
import os.path
import subprocess
import tempfile
from time import sleep
from PIL import Image, ImageStat

WEBCAM_PROBES = 1


class WebcamStrategy:
    def __init__(self, config):
        self.config = config
        self.lux = None

        self.capture_command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "panic",
            "-i",
            self.config.input,
            "-vframes",
            "1",
        ]

        self.get_sleep_time()

        if self.config.verbose:
            print("Sleep mode: {} will be use".format(self.config.sleep_mode))

    def get_brighness(self, screenshot_cmd):
        """
        Return brighness from a webcam capture
        """
        f, path = tempfile.mkstemp()
        os.close(f)
        os.remove(path)

        path += ".jpg"
        try:
            subprocess.run([*screenshot_cmd, path], check=True)
        except FileNotFoundError as e:
            raise ("The binary is not found?\n{}".format(e))

        result = None
        with Image.open(path) as im:
            stat = ImageStat.Stat(im)
            r, g, b = stat.rms
            result = math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))

        os.remove(path)
        return int(100 * (result / 255))

    def calculate(self):
        """
        Fetch the brighness WEBCAM_PROBES time
        And return the average
        """
        results = []
        for _ in range(0, WEBCAM_PROBES):
            results.append(self.get_brighness(self.capture_command))
            sleep(1)
        return int(sum(results) / float(len(results)))

    def get_sleep_time(self):
        """
        Return how many time to sleep between two loop
        """
        self.sleep_time = self.config.sleep_time
        if self.config.sleep_mode == "fixed":
            self.sleep_time = self.config.sleep_time
        elif self.config.sleep_mode == "periods":
            self.sleep_time = self.config.get_sleep_by_periods()
        elif self.config.sleep_mode == "lux" and self.lux:
            # less refresh in the dark
            self.sleep_time = (
                (self.config.sleep_time * 2)
                if self.lux <= 10
                else self.config.sleep_time
            )

            # more refresh if very bright
            self.sleep_time = (
                (self.config.sleep_time * 0.5)
                if self.lux >= 80
                else self.config.sleep_time
            )
        if WEBCAM_PROBES > 1:
            self.sleep_time = self.sleep_time - WEBCAM_PROBES

    def run(self):
        # get sensor value
        try:
            self.lux = self.calculate()
        except subprocess.CalledProcessError as e:
            raise ("Can't get lux, bad input device?\n{}".format(e))

        self.get_sleep_time()

        if self.config.verbose:
            print("lux={} | waiting {} seconds...".format(self.lux, self.sleep_time))
