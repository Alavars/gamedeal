from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.cheapshark import cheapshark
from src.database.connection import get_db
from sqlalchemy.orm import Session
from src.routes.wishlist import get_current_user
from fastapi import Depends
from src.services.analytics import calculate_game_stats

router = APIRouter(prefix="/deals", tags=["deals"])
templates = Jinja2Templates(directory="templates")

@router.get("/search", response_class=HTMLResponse)
async def search_deals(request: Request, query: str = Query("")):
    if not query or len(query) < 3:
        return "<!-- Please enter at least 3 characters -->"
        
    try:
        results = await cheapshark.search_games(title=query)
        # In a real app we'd map these to nice HTML, here we just return a simple list for the MVP scaffold
        html_response = "<div class='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>"
        for game in results:
            html_response += f"""
            <div class='bg-white rounded-lg shadow-md overflow-hidden flex'>
                <img src='{game.get("thumb")}' alt='{game.get("external")}' class='w-32 h-32 object-cover'>
                <div class='p-4 flex flex-col justify-between w-full'>
                    <h3 class='font-bold text-lg truncate' title='{game.get("external")}'>{game.get("external")}</h3>
                    <p class='text-green-600 font-bold'>Best Price: ${game.get("cheapest")}</p>
                    <a href='/deals/{game.get("gameID")}' class='mt-2 text-sm text-center bg-blue-100 text-blue-700 py-1 rounded hover:bg-blue-200'>View Details</a>
                </div>
            </div>
            """
        html_response += "</div>"
        
        if not results:
            html_response = "<p class='text-center text-gray-500'>No games found.</p>"
            
        return html_response
    except Exception as e:
        return f"<p class='text-red-500'>Error fetching deals: {str(e)}</p>"

@router.get("/{game_id}", response_class=HTMLResponse)
async def get_game_details(request: Request, game_id: str, db: Session = Depends(get_db)):
    try:
        # Assuming cheapshark service has get_game_details
        game_data = await cheapshark.get_game_details(game_id)
        
        # Calculate stats using pandas
        stats = calculate_game_stats(game_data.get('deals', []))
        
        user = get_current_user(request, db)
        return templates.TemplateResponse(
            "game_details.html", 
            {"request": request, "game": game_data, "user": user, "game_id": game_id, "stats": stats}
        )
    except Exception as e:
        return f"<p class='text-red-500'>Error fetching details: {str(e)}</p>"
