import time
import warnings

from logic.core.lifecycle_group import LifecycleGroup


class Timer:
    def __init__(self, duration: float|None = None): #duration = None если мы просто хотим считать время
        self.__duration = duration
        self.__start_time: float|None = None
        self.__pause_time: float|None = None

    def is_running(self):
        return self.__start_time is not None

    def start(self, group: LifecycleGroup):
        if self.is_running():
            warnings.warn("Timer is already running!")
            return
        group.register_timer(timer=self)
        self.__start_time = time.time()

    def stop(self, group: LifecycleGroup):
        if not self.is_running():
            warnings.warn("Timer is already stopped!")
            return
        self.__start_time = None
        group.unregister_timer(timer=self)

    def get_time(self):
        if not self.is_running():
            warnings.warn("Timer is stopped! Start the timer first!")
            return 0
        current_time = self.__start_time
        if self.__pause_time is None:
            return time.time() - current_time
        else:            
            return self.__pause_time - current_time

    def set_duration(self, duration: float):
        self.__duration = duration

    def is_completed(self):
        if self.__duration is None:
            return False
        else:
            return self.get_time() >= self.__duration

    def pause(self, is_paused: bool):
        if is_paused and self.__pause_time is None:
            self.__pause_time = time.time()
        if not is_paused and self.__pause_time is not None:
            if self.__start_time is not None:
                diff = time.time() - self.__pause_time
                self.__start_time += diff
            self.__pause_time = None
