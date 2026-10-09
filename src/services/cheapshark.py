import httpx
from src.config import settings

class CheapSharkClient:
    def __init__(self):
        self.base_url = settings.cheapshark_base_url
        self.headers = {"User-Agent": "GameDealApp/1.0 (contact@example.com)"}

    async def search_games(self, title: str, limit: int = 10):
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(
                f"{self.base_url}/games",
                params={"title": title, "limit": limit}
            )
            response.raise_for_status()
            return response.json()
            
    async def get_game_details(self, game_id: str):
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(
                f"{self.base_url}/games",
                params={"id": game_id}
            )
            response.raise_for_status()
            return response.json()

cheapshark = CheapSharkClient()
