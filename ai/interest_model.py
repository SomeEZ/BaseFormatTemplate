import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, Optional


class InterestModel:
    DECAY_RATE = 0.95
    
    def __init__(self, db_path: str = "ai_data/interest.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interests (
                group_id TEXT,
                topic TEXT,
                weight REAL,
                last_update TIMESTAMP,
                PRIMARY KEY (group_id, topic)
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_topic(self, group_id: str, topic: str, weight: float = 0.1):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO interests 
            (group_id, topic, weight, last_update)
            VALUES (?, ?, ?, ?)
        ''', (group_id, topic, weight, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def update_topic(self, group_id: str, topic: str, delta: float):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT weight FROM interests WHERE group_id = ? AND topic = ?
        ''', (group_id, topic))
        row = cursor.fetchone()
        
        if row:
            new_weight = max(0.01, min(1.0, row[0] + delta))
            cursor.execute('''
                UPDATE interests SET weight = ?, last_update = ?
                WHERE group_id = ? AND topic = ?
            ''', (new_weight, datetime.now().isoformat(), group_id, topic))
        else:
            cursor.execute('''
                INSERT INTO interests 
                (group_id, topic, weight, last_update)
                VALUES (?, ?, ?, ?)
            ''', (group_id, topic, max(0.01, delta), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_interests(self, group_id: str) -> Dict[str, float]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT topic, weight, last_update FROM interests WHERE group_id = ?
        ''', (group_id,))
        
        interests = {}
        now = datetime.now()
        for topic, weight, last_update in cursor.fetchall():
            update_time = datetime.fromisoformat(last_update)
            days_passed = (now - update_time).days
            decayed_weight = weight * (self.DECAY_RATE ** days_passed)
            
            if decayed_weight > 0.01:
                interests[topic] = decayed_weight
        
        conn.close()
        self._normalize_weights(group_id, interests)
        return interests
    
    def _normalize_weights(self, group_id: str, interests: Dict[str, float]):
        total = sum(interests.values())
        if total > 0:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            for topic, weight in interests.items():
                normalized = weight / total
                cursor.execute('''
                    UPDATE interests SET weight = ?
                    WHERE group_id = ? AND topic = ?
                ''', (normalized, group_id, topic))
            conn.commit()
            conn.close()
    
    def match_topic(self, group_id: str, message: str) -> float:
        interests = self.get_interests(group_id)
        if not interests:
            return 0.15
        
        max_match = 0.15
        message_lower = message.lower()
        
        for topic, weight in interests.items():
            if topic.lower() in message_lower:
                similarity = weight * 0.8 + 0.2
                max_match = max(max_match, similarity)
        
        return max_match
    
    def cold_start(self, group_id: str, topics: list):
        for topic in topics:
            self.add_topic(group_id, topic, weight=0.1)
