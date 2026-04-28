from .abc_time_info import ABCTimeInfo
from .abc_basic_info import ABCBasicInfo
from .abc_group_info import ABCGroupInfo
from .abc_message_info import ABCMessageInfo
from .abc_sender_info import ABCSenderInfo
from .time_info import TimeInfo
from .basic_info import BasicInfo
from .group_info import GroupInfo
from .message_info import MessageInfo
from .sender_info import SenderInfo


class LotteryFactory:
    @staticmethod
    def create_time_info(timestamp: int) -> ABCTimeInfo:
        return TimeInfo(timestamp)

    @staticmethod
    def create_basic_info(self_id: int, platform: str, post_type: str, message_type: str, sub_type: str) -> ABCBasicInfo:
        return BasicInfo(self_id, platform, post_type, message_type, sub_type)

    @staticmethod
    def create_group_info(group_id: int, group_name: str) -> ABCGroupInfo:
        return GroupInfo(group_id, group_name)

    @staticmethod
    def create_message_info(message_id: str, message_seq: int, real_id: int, real_seq: int) -> ABCMessageInfo:
        return MessageInfo(message_id, message_seq, real_id, real_seq)

    @staticmethod
    def create_sender_info(user_id: int, nickname: str, card: str, role: str, sex: str = None) -> ABCSenderInfo:
        return SenderInfo(user_id, nickname, card, role, sex)
