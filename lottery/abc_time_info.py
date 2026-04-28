from abc import ABC, abstractmethod


class ABCTimeInfo(ABC):
    @abstractmethod
    def get_formatted_time(self) -> str:
        pass

    @abstractmethod
    def get_timestamp(self) -> int:
        pass
