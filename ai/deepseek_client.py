import aiohttp
from typing import List, Dict, Optional, AsyncGenerator


class DeepSeekClient:
    BASE_URL = "https://api.deepseek.com"
    
    def __init__(self, api_key: str, model: str = "deepseek-v4-flash"):
        self.api_key = api_key
        self.model = model
        self.session = None
    
    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        thinking: bool = False,
        reasoning_effort: str = "medium",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False
    ):
        session = await self._get_session()
        
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)
        
        payload = {
            "model": self.model,
            "messages": full_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        if thinking:
            payload["thinking"] = {"type": "enabled"}
            payload["reasoning_effort"] = reasoning_effort
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        if stream:
            return self._stream_chat(session, payload, headers)
        else:
            return await self._non_stream_chat(session, payload, headers)
    
    async def _non_stream_chat(self, session, payload, headers):
        async with session.post(
            f"{self.BASE_URL}/chat/completions",
            headers=headers,
            json=payload
        ) as response:
            data = await response.json()
            if "error" in data:
                raise Exception(f"DeepSeek API Error: {data['error']}")
            return {
                "content": data["choices"][0]["message"]["content"],
                "thinking": data["choices"][0]["message"].get("thinking_content", ""),
                "usage": data.get("usage", {}),
                "model": data.get("model", self.model)
            }
    
    async def _stream_chat(self, session, payload, headers) -> AsyncGenerator[Dict[str, str], None]:
        payload["stream"] = True
        async with session.post(
            f"{self.BASE_URL}/chat/completions",
            headers=headers,
            json=payload
        ) as response:
            async for line in response.content:
                line = line.decode('utf-8').strip()
                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break
                    import json
                    try:
                        chunk = json.loads(data)
                        if 'choices' in chunk and len(chunk['choices']):
                            delta = chunk['choices'][0].get('delta', {})
                            yield {
                                'content': delta.get('content', ''),
                                'thinking': delta.get('thinking_content', ''),
                                'usage': chunk.get('usage', None)
                            }
                    except:
                        pass
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
