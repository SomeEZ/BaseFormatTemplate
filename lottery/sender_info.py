from .abc_sender_info import ABCSenderInfo


class SenderInfo(ABCSenderInfo):
    _SEX_MAP = {"unknown": "未知", "male": "男", "female": "女"}
    _ROLE_MAP = {"owner": "群主", "admin": "管理员", "member": "成员"}
    _NONE_MAP = {None: "无"}

    def __init__(self, user_id: int, nickname: str, card: str, role: str, sex: str = None):
        self._user_id = user_id
        self._nickname = nickname
        self._card = card
        self._role = role
        self._sex = sex

    @staticmethod
    def _translate(value, map_dict):
        if value in map_dict:
            return map_dict[value]
        if value is None:
            return "无"
        return value

    def get_user_id(self) -> int:
        return self._user_id

    def get_nickname(self) -> str:
        return self._nickname

    def get_card(self) -> str:
        return self._translate(self._card, self._NONE_MAP)

    def get_role(self) -> str:
        return self._translate(self._role, self._ROLE_MAP)

    def get_sex(self) -> str:
        return self._translate(self._sex, self._SEX_MAP)

    def get_user_name(self) -> str:
        return self._card or self._nickname
