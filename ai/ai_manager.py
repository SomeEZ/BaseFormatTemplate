from typing import Dict, List, Optional
from collections import defaultdict
from .deepseek_client import DeepSeekClient
from .chronotype import Chronotype
from .interest_model import InterestModel
from .heat_monitor import HeatMonitor
from .fatigue_manager import FatigueManager
from .decision_engine import DecisionEngine
from .active_speaker import ActiveSpeaker


class AIManager:
    def __init__(self, api_key: str, model: str = "deepseek-v4-flash", persona: str = 'normal'):
        self.client = DeepSeekClient(api_key, model)
        self.conversation_history: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        self.max_history = 20
        
        self.chronotype = Chronotype(persona=persona)
        self.interest_model = InterestModel()
        self.heat_monitor = HeatMonitor()
        self.fatigue_manager = FatigueManager(persona=persona)
        self.decision_engine = DecisionEngine(persona=persona)
        self.active_speaker = ActiveSpeaker()
        
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
    
    def should_reply(
        self,
        group_id: str,
        message: str,
        is_at_mentioned: bool = False
    ) -> Dict:
        self.heat_monitor.record_message(group_id)
        
        activity = self.chronotype.get_activity()
        match_score = self.interest_model.match_topic(group_id, message)
        heat_factor = self.heat_monitor.get_heat_factor(group_id)
        fatigue = self.fatigue_manager.get_fatigue(group_id)
        is_on_cooldown = self.fatigue_manager.is_on_cooldown(group_id)
        
        decision = self.decision_engine.get_decision(
            activity=activity,
            match_score=match_score,
            heat_factor=heat_factor,
            fatigue=fatigue,
            is_at_mentioned=is_at_mentioned,
            is_on_cooldown=is_on_cooldown
        )
        
        return decision
    
    def record_reply(self, group_id: str):
        self.fatigue_manager.record_reply(group_id)
    
    def update_interest(self, group_id: str, message: str):
        keywords = ['python', '编程', '技术', '游戏', '音乐', '电影', '学习', '工作']
        for keyword in keywords:
            if keyword in message.lower():
                self.interest_model.update_topic(group_id, keyword, 0.1)
    
    async def try_active_speak(self, group_id: str):
        activity = self.chronotype.get_activity()
        is_cold = self.heat_monitor.is_cold(group_id)
        return await self.active_speaker.try_active_speak(group_id, activity, is_cold)
    
    def clear_history(self, user_id: str, group_id: Optional[str] = None):
        key = self._get_conversation_key(user_id, group_id)
        self.conversation_history[key].clear()
        return True
    
    async def close(self):
        await self.client.close()
