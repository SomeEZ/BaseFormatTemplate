from .abc_basic_info import ABCBasicInfo


class BasicInfo(ABCBasicInfo):
    _PLATFORM_MAP = {"qq": "QQ"}
    _POST_TYPE_MAP = {"message": "消息"}
    _MESSAGE_TYPE_MAP = {"group": "群聊", "private": "私聊"}
    _SUB_TYPE_MAP = {"normal": "普通"}

    def __init__(self, self_id: int, platform: str, post_type: str, message_type: str, sub_type: str):
        self._self_id = self_id
        self._platform = platform
        self._post_type = post_type
        self._message_type = message_type
        self._sub_type = sub_type

    @staticmethod
    def _translate(value, map_dict):
        if value in map_dict:
            return map_dict[value]
        if value is None:
            return "无"
        return value

    def get_self_id(self) -> int:
        return self._self_id

    def get_platform(self) -> str:
        return self._translate(self._platform, self._PLATFORM_MAP)

    def get_post_type(self) -> str:
        return self._translate(self._post_type, self._POST_TYPE_MAP)

    def get_message_type(self) -> str:
        return self._translate(self._message_type, self._MESSAGE_TYPE_MAP)

    def get_sub_type(self) -> str:
        return self._translate(self._sub_type, self._SUB_TYPE_MAP)
