import httpx
import asyncio

async def test():
    async with httpx.AsyncClient(headers={'User-Agent': 'GameDealPulse/1.0'}) as client:
        resp = await client.get('https://www.cheapshark.com/api/1.0/games?id=262193')
        details = resp.json()
        for d in details['deals']:
            print(f'Store ID {d[\"storeID\"]}: ')

asyncio.run(test())