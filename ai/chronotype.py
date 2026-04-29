import time
import random
from datetime import datetime


class Chronotype:
    def __init__(self, timezone=8, persona='normal'):
        self.timezone = timezone
        self.persona = persona
        
    def get_activity(self) -> float:
        now = datetime.now()
        hour = now.hour + self.timezone
        
        if self.persona == 'night_owl':
            return self._night_owl_profile(hour)
        elif self.persona == 'workaholic':
            return self._workaholic_profile(hour)
        else:
            return self._normal_profile(hour)
    
    def _normal_profile(self, hour: int) -> float:
        hour = hour % 24
        
        if 0 <= hour < 6:
            return 0.1 + random.uniform(-0.05, 0.05)
        elif 6 <= hour < 9:
            return 0.3 + (hour - 6) * 0.2 + random.uniform(-0.05, 0.05)
        elif 9 <= hour < 12:
            return 0.9 + random.uniform(-0.05, 0.05)
        elif 12 <= hour < 14:
            return 0.75 + random.uniform(-0.05, 0.05)
        elif 14 <= hour < 18:
            return 0.85 + random.uniform(-0.05, 0.05)
        elif 18 <= hour < 22:
            return 0.95 + random.uniform(-0.05, 0.05)
        elif 22 <= hour < 24:
            return 0.6 - (hour - 22) * 0.25 + random.uniform(-0.05, 0.05)
        
        return 0.1
    
    def _night_owl_profile(self, hour: int) -> float:
        hour = hour % 24
        
        if 0 <= hour < 8:
            return 0.8 - (hour % 8) * 0.1 + random.uniform(-0.05, 0.05)
        elif 8 <= hour < 14:
            return 0.2 + random.uniform(-0.05, 0.05)
        elif 14 <= hour < 18:
            return 0.5 + random.uniform(-0.05, 0.05)
        elif 18 <= hour < 24:
            return 0.9 + random.uniform(-0.05, 0.05)
        
        return 0.8
    
    def _workaholic_profile(self, hour: int) -> float:
        hour = hour % 24
        
        if 0 <= hour < 5:
            return 0.3 + random.uniform(-0.05, 0.05)
        elif 5 <= hour < 8:
            return 0.5 + random.uniform(-0.05, 0.05)
        elif 8 <= hour < 22:
            return 0.95 + random.uniform(-0.05, 0.05)
        elif 22 <= hour < 24:
            return 0.7 - (hour - 22) * 0.2 + random.uniform(-0.05, 0.05)
        
        return 0.3
    
    def is_sleeping(self) -> bool:
        return self.get_activity() < 0.2
