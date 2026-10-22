import httpx
from src.config import settings

class CheapSharkClient:
    def __init__(self):
        self.base_url = settings.cheapshark_base_url
        self.headers = {"User-Agent": "GameDealPulse-App/2.4 (gamedealpulse.support@proton.me)"}
        self.timeout = httpx.Timeout(15.0, connect=5.0)
        self._stores = {}

    def _normalize_thumb(self, thumb: str, steam_app_id: str = None) -> str:
        if not thumb and steam_app_id:
            return f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{steam_app_id}/capsule_231x87.jpg"
        if not thumb:
            return ""
        thumb = thumb.strip()
        if thumb.startswith("//"):
            return f"https:{thumb}"
        return thumb

    async def get_stores(self):
        if not self._stores:
            try:
                async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                    resp = await client.get(f"{self.base_url}/stores")
                    if resp.status_code == 200:
                        for store in resp.json():
                            self._stores[str(store['storeID'])] = store['storeName']
            except Exception:
                pass
        return self._stores

    async def search_games(self, title: str, limit: int = 12):
        cleaned_title = title.strip()
        if not cleaned_title:
            return []

        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            deals = []
            try:
                response = await client.get(
                    f"{self.base_url}/deals",
                    params={"title": cleaned_title, "pageSize": limit * 2}
                )
                if response.status_code == 200:
                    deals = response.json()
            except Exception:
                deals = []
            
            stores = await self.get_stores()
            unique_games = {}

            # Populate from deals first
            if isinstance(deals, list):
                for deal in deals:
                    game_id = str(deal.get('gameID', ''))
                    if not game_id or game_id in unique_games:
                        continue
                    thumb = self._normalize_thumb(deal.get('thumb', ''), deal.get('steamAppID'))
                    unique_games[game_id] = {
                        "gameID": game_id,
                        "external": deal.get('title') or 'Unknown Title',
                        "thumb": thumb,
                        "cheapest": str(deal.get('salePrice') or '0.00'),
                        "cheapestDealID": deal.get('dealID') or '',
                        "cheapest_store_name": stores.get(str(deal.get('storeID')), f"Store {deal.get('storeID', '')}")
                    }

            # If fewer results than requested or none found, fallback to /games endpoint
            if len(unique_games) < limit:
                try:
                    resp_games = await client.get(
                        f"{self.base_url}/games",
                        params={"title": cleaned_title, "limit": limit}
                    )
                    if resp_games.status_code == 200:
                        games_data = resp_games.json()
                        if isinstance(games_data, list):
                            for g in games_data:
                                g_id = str(g.get('gameID', ''))
                                if not g_id or g_id in unique_games:
                                    continue
                                thumb = self._normalize_thumb(g.get('thumb', ''), g.get('steamAppID'))
                                unique_games[g_id] = {
                                    "gameID": g_id,
                                    "external": g.get('external') or 'Unknown Title',
                                    "thumb": thumb,
                                    "cheapest": str(g.get('cheapest') or '0.00'),
                                    "cheapestDealID": g.get('cheapestDealID') or '',
                                    "cheapest_store_name": "Store"
                                }
                except Exception:
                    pass

            return list(unique_games.values())[:limit]
            
    async def get_top_deals(self, limit: int = 6):
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/deals",
                    params={"sortBy": "Deal Rating", "pageSize": limit}
                )
                if response.status_code != 200:
                    return []
                deals = response.json()
            except Exception:
                return []
            
            stores = await self.get_stores()
            formatted = []
            if isinstance(deals, list):
                for deal in deals:
                    thumb = self._normalize_thumb(deal.get('thumb', ''), deal.get('steamAppID'))
                    formatted.append({
                        "gameID": str(deal.get('gameID', '')),
                        "external": deal.get('title') or 'Unknown Title',
                        "thumb": thumb,
                        "cheapest": str(deal.get('salePrice') or '0.00'),
                        "cheapestDealID": deal.get('dealID') or '',
                        "cheapest_store_name": stores.get(str(deal.get('storeID')), f"Store {deal.get('storeID', '')}")
                    })
            return formatted

    async def get_game_details(self, game_id: str):
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/games",
                    params={"id": game_id}
                )
                if response.status_code in [404, 429]:
                    return {
                        "info": {"title": f"Game #{game_id}", "thumb": ""},
                        "cheapestPriceEver": {"price": "N/A", "date": 0},
                        "deals": []
                    }
                response.raise_for_status()
                data = response.json()
            except Exception:
                return {
                    "info": {"title": f"Game #{game_id}", "thumb": ""},
                    "cheapestPriceEver": {"price": "N/A", "date": 0},
                    "deals": []
                }
            
            # Map store names and fix thumb
            info = data.get('info', {})
            info['thumb'] = self._normalize_thumb(info.get('thumb', ''), info.get('steamAppID'))

            stores = await self.get_stores()
            for deal in data.get('deals', []):
                deal['store_name'] = stores.get(str(deal.get('storeID')), f"Store {deal.get('storeID')}")
                
            return data

cheapshark = CheapSharkClient()
