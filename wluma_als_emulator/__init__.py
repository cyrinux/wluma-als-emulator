#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


try:
    from setproctitle import setproctitle

    setproctitle("wluma-als-emulator")
except ImportError:
    pass


def main():
    from .core.sensor import Sensor
    from .core.config import Config

    try:
        config = Config()
        if config.strategy == "time":
            from .strategies.time_strategy import TimeStrategy

            strategy = TimeStrategy(config)
        elif config.strategy == "webcam":
            from .strategies.webcam_strategy import WebcamStrategy

            strategy = WebcamStrategy(config)
        elif config.strategy == "noon":
            from .strategies.noon_strategy import NoonStrategy

            strategy = NoonStrategy(config)
        elif config.strategy == "daylight":
            from .strategies.daylight_strategy import DayLightStrategy

            strategy = DayLightStrategy(config)
        else:
            config.usage()
            sys.exit(1)

        fals = Sensor(strategy)
        fals.run()

    except Exception as e:
        raise ("Got exception, aborting: ", e)
        try:
            fals.cleanup()
        except:
            pass
        sys.exit(3)


if __name__ == "__main__":
    main()
