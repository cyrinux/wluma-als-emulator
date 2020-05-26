from datetime import datetime, time


class TimeStrategy:
    def __init__(self, config):
        """
        we take current time (say 11:10am), convert to seconds (11*60*60 + 10*60 = 40200),
        and then because midday (43200s) is 100% lux and midnight (0s) is 0% lux,
        change of 1% of lux is (43200 / 100 = 432),
        current time 11am should be (100 - (43200 - 40200) / 432) = 93% of lux
        """
        self.config = config
        self.lux = None
        self.sleep_time = self.config.sleep_time

    def calculate(self):
        midday_in_seconds = 43200
        datenow = datetime.now()
        midnight = datetime.combine(datenow.date(), time(0))
        now = datenow - midnight
        now_in_seconds = now.seconds
        # from midnight to midday lux up
        if now_in_seconds > midday_in_seconds:
            lux = 100 - ((now_in_seconds * 100 / midday_in_seconds) - 100)
        else:
            # after midday to midnight lux down
            lux = now_in_seconds * 100 / midday_in_seconds
        return int(lux)

    def run(self):
        self.lux = self.calculate()

        if self.config.verbose:
            print(f"lux={self.lux} | waiting {self.sleep_time} seconds...")
