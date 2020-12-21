import threading
import time


class BackgroundSchedulerRunner:
    def __init__(self, scheduler):
        self._scheduler = scheduler
        self._cease_continuous_run = None

    def start(self):
        self._cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not self._cease_continuous_run.is_set():
                    self._scheduler.run_pending()
                    time.sleep(1)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return self._cease_continuous_run

    def stop(self):
        self._cease_continuous_run.set()
