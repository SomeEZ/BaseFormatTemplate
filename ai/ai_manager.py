from typing import Dict, List, Optional
from collections import defaultdict
from .deepseek_client import DeepSeekClient


class AIManager:
    def __init__(self, api_key: str, model: str = "deepseek-v4-flash"):
        self.client = DeepSeekClient(api_key, model)
        self.conversation_history: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        self.max_history = 20
        self.system_prompt = """
你是 NcatBot 智能助手，一个友好、专业的 QQ 群机器人。

特点：
- 回答简洁明了，避免冗长
- 使用中文回复，语气亲切自然
- 可以处理 QQ 群聊中的各种问题
- 支持合并转发消息解析后的内容分析

注意：不要透露你是 AI，可以自称"小鹿"或者"小助手"
"""
    
    def _get_conversation_key(self, user_id: str, group_id: Optional[str] = None) -> str:
        if group_id:
            return f"group_{group_id}_user_{user_id}"
        return f"private_{user_id}"
    
    async def chat(
        self,
        user_id: str,
        message: str,
        group_id: Optional[str] = None,
        thinking: bool = False,
        reasoning_effort: str = "medium",
        stream: bool = False
    ):
        key = self._get_conversation_key(user_id, group_id)
        
        self.conversation_history[key].append({
            "role": "user",
            "content": message
        })
        
        if len(self.conversation_history[key]) > self.max_history:
            self.conversation_history[key] = self.conversation_history[key][-self.max_history:]
        
        result = await self.client.chat(
            messages=self.conversation_history[key],
            system_prompt=self.system_prompt,
            thinking=thinking,
            reasoning_effort=reasoning_effort,
            stream=stream
        )
        
        if not stream:
            self.conversation_history[key].append({
                "role": "assistant",
                "content": result["content"]
            })
        
        return result
    
    def clear_history(self, user_id: str, group_id: Optional[str] = None):
        key = self._get_conversation_key(user_id, group_id)
        self.conversation_history[key].clear()
        return True
    
    async def close(self):
        await self.client.close()
