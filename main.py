from ncatbot.core import registrar
from ncatbot.event.qq import GroupMessageEvent, PrivateMessageEvent
from ncatbot.plugin import NcatBotPlugin
from ncatbot.utils import get_log
from .lottery import LotteryData
from .saveMessage import save_message
from .ai import AIManager
from .utils import NapCatAPI

LOG = get_log("BaseFormatTemplate")

DEEPSEEK_API_KEY = "sk-0052a2da82164e2190dc76608b38ecc0"
AI_TRIGGER = "小鹿"
AI_MODEL = "deepseek-v4-flash"


class BaseFormatTemplate(NcatBotPlugin):
    name = "BaseFormatTemplate"
    version = "1.1.0"
    author = "NcatBot"
    description = "Base Format Template + DeepSeek AI - ABC 抽象封装 + DeepSeek 智能对话"

    def __init__(self):
        super().__init__()
        self.ai_manager = None

    async def on_load(self):
        LOG.info("BaseFormatTemplate plugin loaded!")
        if DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "sk-your-api-key-here":
            self.ai_manager = AIManager(DEEPSEEK_API_KEY, AI_MODEL)
            LOG.info(f"DeepSeek AI 已启用，模型: {AI_MODEL}")
        else:
            LOG.warning("未配置 DeepSeek API Key，AI 功能未启用")

    async def on_close(self):
        LOG.info("BaseFormatTemplate plugin unloaded!")
        if self.ai_manager:
            await self.ai_manager.close()

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
        at_users = lottery.message_info.get_at_users()
        if at_users:
            print(f"    ├── @用户: {', '.join(at_users)}")
        if lottery.message_info.is_at_all():
            print(f"    ├── @全体: 是")
        if lottery.message_info.has_reply():
            print(f"    ├── 引用回复ID: {lottery.message_info.get_reply_message_id()}")
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

        if self.ai_manager:
            bot_id = str(lottery.basic_info.get_self_id())
            is_at_bot = lottery.message_info.is_at_user(bot_id)
            has_deer_keyword = "小鹿" in text_content
            has_reply = lottery.message_info.has_reply()
            
            if is_at_bot or has_deer_keyword or (has_reply and text_content and text_content != "无"):
                thinking_msg_id = None
                try:
                    thinking_msg = await event.reply(text="⏳ 深度思考中...")
                    thinking_msg_id = getattr(thinking_msg, 'message_id', None) or getattr(thinking_msg, 'id', None)
                    
                    ai_message = ""
                    if has_reply:
                        ai_message += "【用户引用回复了之前的消息】\n"
                        ai_message += f"用户说: {text_content}\n"
                        ai_message += "请结合上下文回答。\n\n"
                    ai_message += text_content
                    
                    if not ai_message.strip():
                        ai_message = "你好呀！"
                    
                    result = await self.ai_manager.chat(
                        user_id=lottery.sender_info.get_user_id(),
                        message=ai_message,
                        group_id=lottery.group_info.get_group_id(),
                        thinking=True,
                        reasoning_effort="high"
                    )
                    
                    if thinking_msg_id:
                        await NapCatAPI.delete_msg(int(thinking_msg_id))
                    
                    await event.reply(text=result['content'])
                    
                    if result['thinking']:
                        LOG.info(f"AI 思考过程: {result['thinking']}")
                    
                except Exception as e:
                    LOG.error(f"AI 回复失败: {e}")
                    if thinking_msg_id:
                        await NapCatAPI.delete_msg(int(thinking_msg_id))
                    await event.reply(text=f"❌ AI 出错了: {str(e)}")

    @registrar.on_group_command("hello", ignore_case=True)
    async def on_hello(self, event: GroupMessageEvent):
        """收到群消息 'hello' 时回复"""
        await self.api.qq.post_group_msg(event.group_id, text="Hello, World! 👋")

    @registrar.on_group_command("清除记忆", ignore_case=True)
    async def on_clear_memory(self, event: GroupMessageEvent):
        """清除 AI 对话记忆"""
        if not self.ai_manager:
            await event.reply(text="❌ AI 功能未配置")
            return
        
        lottery = LotteryData(event)
        user_id = lottery.sender_info.get_user_id()
        group_id = lottery.group_info.get_group_id()
        
        self.ai_manager.clear_history(user_id, group_id)
        await event.reply(text="✅ 对话记忆已清除！")

    @registrar.on_private_message()
    async def on_private_ai_chat(self, event: PrivateMessageEvent):
        """私聊自动触发 AI 对话"""
        if not self.ai_manager:
            await event.reply(text="❌ AI 功能未配置，请设置 DeepSeek API Key")
            return
        
        lottery = LotteryData(event)
        user_id = lottery.sender_info.get_user_id()
        user_message = lottery.message_info.get_text_content()
        has_reply = lottery.message_info.has_reply()
        
        if not user_message or user_message == "无":
            if has_reply:
                user_message = "（引用回复了消息）"
            else:
                await event.reply(text="🤔 请输入您的问题")
                return
        
        thinking_msg_id = None
        try:
            thinking_msg = await event.reply(text="⏳ 深度思考中...")
            thinking_msg_id = getattr(thinking_msg, 'message_id', None) or getattr(thinking_msg, 'id', None)
            
            ai_message = ""
            if has_reply:
                ai_message += "【私聊中用户引用回复了之前的消息】\n"
                ai_message += f"用户说: {user_message}\n"
                ai_message += "请结合上下文回答。\n\n"
            ai_message += user_message
            
            result = await self.ai_manager.chat(
                user_id=user_id,
                message=ai_message,
                group_id=None,
                thinking=True,
                reasoning_effort="high"
            )
            
            if thinking_msg_id:
                await NapCatAPI.delete_msg(int(thinking_msg_id))
            
            await event.reply(text=result['content'])
            
        except Exception as e:
            LOG.error(f"AI 私聊回复失败: {e}")
            if thinking_msg_id:
                await NapCatAPI.delete_msg(int(thinking_msg_id))
            await event.reply(text=f"❌ AI 出错了: {str(e)}")

    @registrar.on_private_command("hello", ignore_case=True)
    async def on_private_hello(self, event: PrivateMessageEvent):
        """收到私聊消息 'hello' 时回复"""
        await event.reply(text="Hello! This is BaseFormatTemplate! 👋")


BasePlugin = BaseFormatTemplate
