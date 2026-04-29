from collections import deque
from datetime import datetime
from typing import Dict


class HeatMonitor:
    WINDOW_SIZE = 120
    
    def __init__(self):
        self.group_windows: Dict[str, deque] = {}
        self.MAX_H = 30
    
    def record_message(self, group_id: str):
        if group_id not in self.group_windows:
            self.group_windows[group_id] = deque(maxlen=self.WINDOW_SIZE)
        
        self.group_windows[group_id].append(datetime.now().timestamp())
    
    def get_heat_factor(self, group_id: str) -> float:
        if group_id not in self.group_windows:
            return 1.0
        
        window = self.group_windows[group_id]
        if not window:
            return 1.0
        
        now = datetime.now().timestamp()
        recent_count = sum(1 for t in window if now - t <= 120)
        
        H = recent_count
        E_hot = max(0.0, 1 - (H / self.MAX_H) ** 1.5)
        
        return E_hot
    
    def is_cold(self, group_id: str) -> bool:
        if group_id not in self.group_windows:
            return False
        
        window = self.group_windows[group_id]
        if not window:
            return False
        
        now = datetime.now().timestamp()
        return now - window[-1] > 300
