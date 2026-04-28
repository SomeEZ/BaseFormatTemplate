from abc import ABC, abstractmethod
from typing import Optional


class ABCGroupInfo(ABC):
    @abstractmethod
    def get_group_id(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_group_name(self) -> str:
        pass
