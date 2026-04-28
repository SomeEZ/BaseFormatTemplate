import time
from .abc_time_info import ABCTimeInfo


class TimeInfo(ABCTimeInfo):
    def __init__(self, timestamp: int):
        self._timestamp = timestamp

    def get_formatted_time(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self._timestamp))

    def get_timestamp(self) -> int:
        return self._timestamp
