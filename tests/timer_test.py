import pytest
from pysweep import timer as module


class TestTimer:
    def test_start(self):
        timer = module.Timer()
        timer.start()

        with pytest.raises(module.TimerError):
            timer.start()

    @pytest.mark.parametrize('init, duration, elapsed', [
        (0, 5, (0, 0, 5)),
        (0, 61, (0, 1, 1)),
        (0, 59 * 60 + 27, (0, 59, 27)),
        (31 * 60 + 15, 59 * 60 + 27, (0, 28, 12)),
        (0, 68 * 60 + 59, (1, 8, 59)),
        (0, 100 * 3600 + 44, (100, 0, 44)),
    ])
    def test_get_elapsed(self, monkeypatch, init, duration, elapsed):
        timer = module.Timer()

        monkeypatch.setattr('time.perf_counter', lambda: init)
        timer.start()

        monkeypatch.setattr('time.perf_counter', lambda: duration)
        assert elapsed == timer.get_elapsed()
