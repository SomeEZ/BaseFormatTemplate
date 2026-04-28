from .abc_time_info import ABCTimeInfo
from .abc_basic_info import ABCBasicInfo
from .abc_group_info import ABCGroupInfo
from .abc_message_info import ABCMessageInfo
from .abc_sender_info import ABCSenderInfo
from .lottery_factory import LotteryFactory


class LotteryData:
    def __init__(self, event):
        self.time_info: ABCTimeInfo = LotteryFactory.create_time_info(event.data.time)
        self.basic_info: ABCBasicInfo = LotteryFactory.create_basic_info(
            self_id=event.data.self_id,
            platform=event.data.platform,
            post_type=event.data.post_type.value,
            message_type=event.data.message_type.value,
            sub_type=event.data.sub_type
        )
        self.group_info: ABCGroupInfo = LotteryFactory.create_group_info(
            group_id=event.data.group_id,
            group_name=event.data.group_name
        )
        self.message_info: ABCMessageInfo = LotteryFactory.create_message_info(
            message_id=event.data.message_id,
            message_seq=event.data.message_seq,
            real_id=event.data.real_id,
            real_seq=event.data.real_seq
        )
        self.message_info.process_message_chain(event.data.message)
        self.sender_info: ABCSenderInfo = LotteryFactory.create_sender_info(
            user_id=event.data.sender.user_id,
            nickname=event.data.sender.nickname,
            card=event.data.sender.card,
            role=event.data.sender.role,
            sex=getattr(event.data.sender, 'sex', None)
        )
