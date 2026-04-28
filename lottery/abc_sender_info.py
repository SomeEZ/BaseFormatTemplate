from abc import ABC, abstractmethod


class ABCSenderInfo(ABC):
    @abstractmethod
    def get_user_id(self) -> int:
        pass

    @abstractmethod
    def get_nickname(self) -> str:
        pass

    @abstractmethod
    def get_card(self) -> str:
        pass

    @abstractmethod
    def get_role(self) -> str:
        pass

    @abstractmethod
    def get_sex(self) -> str:
        pass

    @abstractmethod
    def get_user_name(self) -> str:
        pass
