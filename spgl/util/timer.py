import time as _time

class Timer():
    def __init__(self, autostart=False):
        """Constructs a new Timer.

        If autostart is true, immediately starts the timer.
        """
        self._start_millis = 0
        self._stop_millis = 0
        self._started = False
        if autostart:
            self.start()

    def elapsed(self):
        return self._stop_millis - self._start_millis

    def is_started(self):
        return self._started

    def start(self):
        self._start_millis = self.current_time_millis()
        self._started = True

    def stop(self):
        self._stop_millis = self.current_time_millis()
        if not self.is_started():
            # error("Timer is not started!")
            self._start_millis = self._stop_millis
        self._started = False
        return self.elapsed()

    @classmethod
    def current_time_millis(cls):
        return int(round(_time.time() * 1000))
