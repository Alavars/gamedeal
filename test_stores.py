import httpx
import asyncio
import json

async def run_test():
    async with httpx.AsyncClient(headers={'User-Agent': 'GameDealPulse/1.0'}) as client:
        # Alan Wake 2 (Epic Games exclusive mostly)
        print("--- Testing Alan Wake 2 (Epic Games) ---")
        resp = await client.get('https://www.cheapshark.com/api/1.0/games?title=Alan Wake 2&limit=1')
        games = resp.json()
        if games:
            game_id = games[0]['gameID']
            print(f"Found: {games[0]['external']} (ID: {game_id})")
            resp2 = await client.get(f'https://www.cheapshark.com/api/1.0/games?id={game_id}')
            details = resp2.json()
            for deal in details['deals']:
                print(f"Store ID {deal['storeID']}: ${deal['price']} (Retail: ${deal['retailPrice']})")
                
        # The Witcher 3
        print("\n--- Testing The Witcher 3 (Multi-store) ---")
        resp = await client.get('https://www.cheapshark.com/api/1.0/games?title=The Witcher 3&limit=1')
        games = resp.json()
        if games:
            game_id = games[0]['gameID']
            print(f"Found: {games[0]['external']} (ID: {game_id})")
            resp2 = await client.get(f'https://www.cheapshark.com/api/1.0/games?id={game_id}')
            details = resp2.json()
            for deal in details['deals'][:5]: # Print top 5 deals
                print(f"Store ID {deal['storeID']}: ${deal['price']} (Retail: ${deal['retailPrice']})")

        # Let's get the list of stores to map IDs to names
        resp_stores = await client.get('https://www.cheapshark.com/api/1.0/stores')
        stores = resp_stores.json()
        print("\n--- Store Map ---")
        for store in stores[:20]:
            print(f"{store['storeID']}: {store['storeName']}")

if __name__ == '__main__':
    asyncio.run(run_test())
