from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List


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

    @abstractmethod
    def get_at_users(self) -> List[str]:
        pass

    @abstractmethod
    def is_at_user(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def is_at_all(self) -> bool:
        pass

    @abstractmethod
    def get_reply_message_id(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_reply_text(self) -> Optional[str]:
        pass

    @abstractmethod
    def has_reply(self) -> bool:
        pass
