import aiohttp
import random
from datetime import datetime, timedelta
from typing import Dict, Optional


class ActiveSpeaker:
    BASE_URL = "http://127.0.0.1:3002"
    
    def __init__(self):
        self.group_last_active: Dict[str, float] = {}
        self.topics = [
            "大家今天工作顺利吗？",
            "有没有什么有趣的事分享一下？",
            "最近在看什么书/剧吗？",
            "讨论一下周末计划吧～",
            "有人想聊技术话题吗？",
            "今天天气不错啊！",
            "大家都在忙什么呢？",
            "有没有什么新发现？",
            "聊点轻松的话题吧～",
            "感觉群里有点安静，出来冒个泡！"
        ]
    
    async def try_active_speak(self, group_id: str, activity: float, is_cold: bool):
        if activity < 0.3:
            return False
        
        if not is_cold:
            return False
        
        if group_id in self.group_last_active:
            last_active = self.group_last_active[group_id]
            if datetime.now().timestamp() - last_active < 1800:
                return False
        
        topic = random.choice(self.topics)
        success = await self._send_group_msg(group_id, topic)
        
        if success:
            self.group_last_active[group_id] = datetime.now().timestamp()
        
        return success
    
    async def _send_group_msg(self, group_id: str, message: str) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.BASE_URL}/send_group_msg",
                    json={"group_id": group_id, "message": message}
                ) as resp:
                    return resp.status == 200
        except Exception:
            return False
