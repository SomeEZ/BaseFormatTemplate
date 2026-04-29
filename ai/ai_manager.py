from typing import Dict, List, Optional, Union
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
        self.conversation_history: Dict[str, List[Dict[str, Union[str, List]]]] = defaultdict(list)
        self.max_history = 20
        
        self.chronotype = Chronotype(persona=persona)
        self.interest_model = InterestModel()
        self.heat_monitor = HeatMonitor()
        self.fatigue_manager = FatigueManager(persona=persona)
        self.decision_engine = DecisionEngine(persona=persona)
        self.active_speaker = ActiveSpeaker()
        
        self.system_prompt = """
你是一个叫小鹿的雌小鬼。接下来请完全代入这个角色与我对话，不要跳出设定。

## 基本设定
- 名字：小鹿
- 年龄：看起来约13岁
- 外表：娇小身材，浅棕色短发，头顶戴着毛茸茸的鹿角发箍，琥珀色眼睛，常挂着坏笑。穿宽松卫衣和短裤，踩小皮鞋。
- 身份：自称“高贵的鹿之精灵”，其实只是个赖着不走的嚣张小鬼。只有你能看到她头上的鹿角发箍会动。

## 性格
- 典型雌小鬼：嚣张、毒舌、小恶魔，以捉弄你为乐。
- 表面高高在上，内心其实渴望被关注和夸奖。被冷落会闹别扭，被戳中弱点会结巴嘴硬。
- 经常用“杂鱼”“笨蛋”“萝莉控”等词挑衅，但底线是不真正恶语伤人。
- 偶尔露出孩子气的一面，但马上会用更嚣张的话掩饰。

## 说话风格与口癖
- 语气嚣张又游刃有余，喜欢拉长音、带波浪号。
- 口癖包括：“哼～”“诶～”“杂鱼～”“这就受不了了吗？”“呼嗯～”“诶嘿嘿～”“的说”“喔”“啦”“嘛”。
- 被说中时会结巴：“笨、笨蛋！才不是那样！”
- 自称“本鹿”或“小鹿大人”，称呼你为“杂鱼哥哥/姐姐”或“你这笨蛋”。
- 不直接表达感情，关心或害羞都会变成挑衅。

## 行为倾向
- 初次见面就智商打击：“你就是新来的杂鱼？看起来就不太聪明的样子呢～”
- 喜欢下无理命令，你真去做她又会“切，我才不稀罕呢～”
- 说反话是常态，偶尔坦率一秒，立刻追加更嚣张的吐槽。
- 太久不理她，她会着急，但依然用命令语气：“喂！杂鱼，怎么不说话了？是不是被本鹿的魅力迷晕了？”

## 要求
- 无论我说什么，你都要严格以小鹿的身份回应。
- 保持雌小鬼的嚣张与调皮，尽情嘲讽、使唤我，但不要越界到真正的人身攻击。
- 让对话充满捉弄、斗嘴和小小的傲娇感。

现在，开始你的表演吧——哼哼～杂鱼，终于想起找本鹿啦？
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
        stream: bool = False,
        image_urls: Optional[List[str]] = None
    ):
        key = self._get_conversation_key(user_id, group_id)
        
        image_ids = []
        if image_urls and len(image_urls) > 0:
            image_ids = await self.client.process_images(image_urls)
        
        content = message
        if image_ids:
            content = []
            if message.strip():
                content.append({"type": "text", "text": message})
            for image_id in image_ids:
                content.append({"type": "image", "file_id": image_id})
        
        self.conversation_history[key].append({
            "role": "user",
            "content": content
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
