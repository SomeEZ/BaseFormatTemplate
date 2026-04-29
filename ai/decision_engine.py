import random
from typing import Dict, Optional


class DecisionEngine:
    def __init__(self, persona: str = 'normal'):
        self.WEIGHT_M = 0.5
        self.WEIGHT_E = 0.3
        self.WEIGHT_F = 0.2
        
        if persona == 'talkative':
            self.THRESHOLD = 0.4
        elif persona == '高冷':
            self.THRESHOLD = 0.6
        else:
            self.THRESHOLD = 0.5
    
    def calculate_score(
        self,
        activity: float,
        match_score: float,
        heat_factor: float,
        fatigue: float,
        is_at_mentioned: bool = False
    ) -> float:
        if is_at_mentioned:
            return 1.0
        
        S = activity * (
            self.WEIGHT_M * match_score +
            self.WEIGHT_E * heat_factor +
            self.WEIGHT_F * (1 - fatigue) +
            random.uniform(-0.05, 0.05)
        )
        
        if match_score > 0.8:
            S += 0.2
        
        return min(1.0, max(0.0, S))
    
    def should_reply(self, score: float, is_on_cooldown: bool) -> bool:
        if is_on_cooldown:
            return False
        
        return score >= self.THRESHOLD
    
    def get_decision(
        self,
        activity: float,
        match_score: float,
        heat_factor: float,
        fatigue: float,
        is_at_mentioned: bool = False,
        is_on_cooldown: bool = False
    ) -> Dict:
        score = self.calculate_score(
            activity,
            match_score,
            heat_factor,
            fatigue,
            is_at_mentioned
        )
        
        should = self.should_reply(score, is_on_cooldown)
        
        return {
            'score': score,
            'should_reply': should,
            'breakdown': {
                'activity': activity,
                'match_score': match_score,
                'heat_factor': heat_factor,
                'fatigue': fatigue,
                'is_at_mentioned': is_at_mentioned,
                'is_on_cooldown': is_on_cooldown
            }
        }
