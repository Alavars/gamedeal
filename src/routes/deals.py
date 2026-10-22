from fastapi import APIRouter, Query, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.database.models import Game
from src.services.cheapshark import cheapshark
from src.services.analytics import calculate_game_stats

router = APIRouter(prefix="/deals", tags=["deals"])

@router.get("/top")
async def get_top_deals(limit: int = 6):
    try:
        deals = await cheapshark.get_top_deals(limit=limit)
        return {"deals": deals}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching top deals: {str(e)}"
        )

@router.get("/search")
async def search_deals(query: str = Query("")):
    if not query or len(query.strip()) < 3:
        return {"results": [], "message": "Query must be at least 3 characters long"}
        
    try:
        results = await cheapshark.search_games(title=query.strip())
        return {"results": results}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching deals: {str(e)}"
        )

@router.get("/{game_id}")
async def get_game_details(game_id: str, db: Session = Depends(get_db)):
    try:
        game_data = await cheapshark.get_game_details(game_id)
        
        # Enrich from local database if available
        local_game = db.query(Game).filter(Game.external_id == game_id).first()
        if local_game:
            info = game_data.setdefault("info", {})
            if not info.get("title") or info.get("title", "").startswith("Game #"):
                info["title"] = local_game.title
            if local_game.thumb_url and not info.get("thumb"):
                info["thumb"] = local_game.thumb_url

        stats = calculate_game_stats(game_data.get('deals', []))
        return {
            "game_id": game_id,
            "game": game_data,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching details: {str(e)}"
        )
