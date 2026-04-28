import aiohttp
from typing import Optional


class NapCatAPI:
    BASE_URL = "http://127.0.0.1:6099"
    
    @staticmethod
    async def delete_msg(message_id: int) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NapCatAPI.BASE_URL}/delete_msg",
                    json={"message_id": message_id}
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            return False
