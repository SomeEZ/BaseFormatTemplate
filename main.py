from ncatbot.core import registrar
from ncatbot.event.qq import GroupMessageEvent, PrivateMessageEvent
from ncatbot.plugin import NcatBotPlugin
from ncatbot.utils import get_log
from .lottery import LotteryData
from .saveMessage import save_message

LOG = get_log("BaseFormatTemplate")


class BaseFormatTemplate(NcatBotPlugin):
    name = "BaseFormatTemplate"
    version = "1.0.0"
    author = "NcatBot"
    description = "Base Format Template - ABC Abstract Encapsulation for Message Fields"

    async def on_load(self):
        LOG.info("BaseFormatTemplate plugin loaded!")

    async def on_close(self):
        LOG.info("BaseFormatTemplate plugin unloaded!")

    @registrar.on_group_message()
    async def on_group_message(self, event: GroupMessageEvent):
        lottery = LotteryData(event)
        
        print("=" * 80)
        print(f"【群消息事件】")
        print(f"  基本信息:")
        print(f"    ├── 时间: {lottery.time_info.get_formatted_time()}")
        print(f"    ├── 时间戳: {lottery.time_info.get_timestamp()}")
        print(f"    ├── 机器人ID: {lottery.basic_info.get_self_id()}")
        print(f"    ├── 平台: {lottery.basic_info.get_platform()}")
        print(f"    ├── 事件类型: {lottery.basic_info.get_post_type()}")
        print(f"    ├── 消息类型: {lottery.basic_info.get_message_type()}")
        print(f"    ├── 子类型: {lottery.basic_info.get_sub_type()}")
        print(f"  群组信息:")
        print(f"    ├── 群ID: {lottery.group_info.get_group_id()}")
        print(f"    └── 群名: {lottery.group_info.get_group_name()}")
        print(f"  消息信息:")
        print(f"    ├── 消息ID: {lottery.message_info.get_message_id()}")
        print(f"    ├── 消息序号: {lottery.message_info.get_message_seq()}")
        print(f"    ├── 真实ID: {lottery.message_info.get_real_id()}")
        print(f"    ├── 真实序号: {lottery.message_info.get_real_seq()}")
        if lottery.message_info.has_forward_message():
            print(f"    ├── 包含合并转发: 是 ({lottery.message_info.get_forward_count()} 条消息)")
        else:
            print(f"    ├── 包含合并转发: 否")
        text_content = lottery.message_info.get_text_content()
        if "合并转发消息" in text_content:
            print(f"    ├── 文字内容: ")
            for i, line in enumerate(text_content.strip().split('\n')):
                prefix = "    │       " if line else "    │"
                print(f"{prefix}{line}")
        else:
            print(f"    ├── 文字内容: {text_content}")
        image_urls = lottery.message_info.get_image_urls()
        if image_urls:
            print(f"    └── 图片链接({lottery.message_info.get_image_count()}张):")
            for i, url in enumerate(image_urls, 1):
                prefix = "        └──" if i == len(image_urls) else "        ├──"
                print(f"{prefix} 图片{i}: {url}")
        else:
            print(f"    └── 图片链接: 无")
        print(f"  发送者信息:")
        print(f"    ├── 用户ID: {lottery.sender_info.get_user_id()}")
        print(f"    ├── 昵称: {lottery.sender_info.get_nickname()}")
        print(f"    ├── 群名片: {lottery.sender_info.get_card()}")
        print(f"    └── 角色: {lottery.sender_info.get_role()}")
        print("=" * 80)
        '''
        # ========== 构建保存的消息内容 ==========
        message_parts = [text_content] if text_content else []
        message_parts.extend([f"[图片{i}]{url}" for i, url in enumerate(image_urls, 1)])
        saved_message = " ".join(message_parts) if message_parts else "无内容"

        # ========== 保存消息 ==========
        saved_path = save_message(
            time=now_time,
            group_id=event.data.group_id,
            group_name=event.data.group_name,
            user_id=str(event.data.sender.user_id),
            user_name=user_name,
            message=saved_message,
            format_type="txt"
        )
        LOG.info(f"消息已保存至: {saved_path}")
        '''
    @registrar.on_group_command("hello", ignore_case=True)
    async def on_hello(self, event: GroupMessageEvent):
        """收到群消息 'hello' 时回复"""
        await self.api.qq.post_group_msg(event.group_id, text="Hello, World! 👋")

    # @registrar.on_group_command("hi", ignore_case=True)
    # async def on_hi(self, event: GroupMessageEvent):
    #     """用 event.reply() 快速回复（自动引用 + @发送者 + 文字）"""
    #     await event.reply(text="你好呀！这是通过 event.reply() 发送的快速回复 🎉")

    @registrar.on_private_command("hello", ignore_case=True)
    async def on_private_hello(self, event: PrivateMessageEvent):
        """收到私聊消息 'hello' 时回复"""
        await event.reply(text="Hello! This is BaseFormatTemplate! 👋")


BasePlugin = BaseFormatTemplate
