from abc import ABC, abstractmethod


class ABCGroupInfo(ABC):
    @abstractmethod
    def get_group_id(self) -> int:
        pass

    @abstractmethod
    def get_group_name(self) -> str:
        pass
