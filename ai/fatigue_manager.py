from datetime import datetime
from typing import Dict, Optional


class FatigueManager:
    def __init__(self, persona: str = 'normal'):
        self.group_fatigue: Dict[str, float] = {}
        self.group_last_reply: Dict[str, float] = {}
        self.persona = persona
        
        if persona == 'talkative':
            self.FATIGUE_INCREMENT = 0.2
            self.FATIGUE_RECOVERY = 0.6
            self.COOLDOWN_SECONDS = 10
        elif persona == '高冷':
            self.FATIGUE_INCREMENT = 0.4
            self.FATIGUE_RECOVERY = 0.3
            self.COOLDOWN_SECONDS = 30
        else:
            self.FATIGUE_INCREMENT = 0.3
            self.FATIGUE_RECOVERY = 0.5
            self.COOLDOWN_SECONDS = 15
    
    def record_reply(self, group_id: str):
        now = datetime.now().timestamp()
        
        if group_id not in self.group_fatigue:
            self.group_fatigue[group_id] = 0.0
        
        self.group_fatigue[group_id] = min(
            1.0,
            self.group_fatigue[group_id] + self.FATIGUE_INCREMENT
        )
        self.group_last_reply[group_id] = now
    
    def get_fatigue(self, group_id: str) -> float:
        self._recover(group_id)
        return self.group_fatigue.get(group_id, 0.0)
    
    def _recover(self, group_id: str):
        if group_id not in self.group_fatigue:
            self.group_fatigue[group_id] = 0.0
            return
        
        if group_id not in self.group_last_reply:
            return
        
        now = datetime.now().timestamp()
        hours_passed = (now - self.group_last_reply[group_id]) / 3600
        
        self.group_fatigue[group_id] = max(
            0.0,
            self.group_fatigue[group_id] - hours_passed * self.FATIGUE_RECOVERY
        )
    
    def is_on_cooldown(self, group_id: str) -> bool:
        if group_id not in self.group_last_reply:
            return False
        
        now = datetime.now().timestamp()
        return now - self.group_last_reply[group_id] < self.COOLDOWN_SECONDS
