from abc import ABC, abstractmethod


class ABCBasicInfo(ABC):
    @abstractmethod
    def get_self_id(self) -> int:
        pass

    @abstractmethod
    def get_platform(self) -> str:
        pass

    @abstractmethod
    def get_post_type(self) -> str:
        pass

    @abstractmethod
    def get_message_type(self) -> str:
        pass

    @abstractmethod
    def get_sub_type(self) -> str:
        pass
