import time
from math import floor


class TimerError(Exception):
    pass


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def get_elapsed(self):
        seconds = round(time.perf_counter() - self._start_time)
        hours, seconds = floor(seconds / 3600), seconds % 3600
        minutes, seconds = floor(seconds / 60), seconds % 60

        return hours, minutes, seconds
