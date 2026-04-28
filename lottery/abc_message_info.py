from abc import ABC, abstractmethod
from typing import Any, Optional


class ABCMessageInfo(ABC):
    @abstractmethod
    def get_message_id(self) -> str:
        pass

    @abstractmethod
    def get_message_seq(self) -> int:
        pass

    @abstractmethod
    def get_real_id(self) -> int:
        pass

    @abstractmethod
    def get_real_seq(self) -> int:
        pass

    @abstractmethod
    def get_text_content(self) -> str:
        pass

    @abstractmethod
    def get_image_urls(self) -> list:
        pass

    @abstractmethod
    def get_image_count(self) -> int:
        pass

    @abstractmethod
    def process_message_chain(self, message_chain: list):
        pass

    @abstractmethod
    def has_forward_message(self) -> bool:
        pass

    @abstractmethod
    def get_forward_count(self) -> int:
        pass

    @abstractmethod
    def process_forward_message(self, msg: Any) -> str:
        pass

    @abstractmethod
    def process_node_message(self, node: Any, depth: int = 1) -> str:
        pass
