from typing import Optional
from .abc_group_info import ABCGroupInfo


class GroupInfo(ABCGroupInfo):
    def __init__(self, group_id: Optional[int] = None, group_name: Optional[str] = None):
        self._group_id = group_id
        self._group_name = group_name

    def get_group_id(self) -> Optional[int]:
        return self._group_id

    def get_group_name(self) -> str:
        return self._group_name or "私聊"
