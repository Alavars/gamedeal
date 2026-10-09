from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.database.models import User, Game, Wishlist

router = APIRouter(prefix="/wishlist", tags=["wishlist"])
templates = Jinja2Templates(directory="templates")

def get_current_user(request: Request, db: Session):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()

@router.get("", response_class=HTMLResponse)
async def view_wishlist(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    
    wishlists = db.query(Wishlist).filter(Wishlist.user_id == user.id).all()
    return templates.TemplateResponse("wishlist.html", {"request": request, "wishlists": wishlists, "user": user})

@router.post("/add")
async def add_to_wishlist(
    request: Request,
    external_id: str = Form(...),
    title: str = Form(...),
    thumb_url: str = Form(""),
    target_price: float = Form(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
        
    # Check if game exists in local DB
    game = db.query(Game).filter(Game.external_id == external_id).first()
    if not game:
        game = Game(external_id=external_id, title=title, thumb_url=thumb_url)
        db.add(game)
        db.commit()
        db.refresh(game)
        
    # Check if already in wishlist
    existing_wishlist = db.query(Wishlist).filter(Wishlist.user_id == user.id, Wishlist.game_id == game.id).first()
    if existing_wishlist:
        existing_wishlist.target_price = target_price
        db.commit()
    else:
        new_wishlist = Wishlist(user_id=user.id, game_id=game.id, target_price=target_price)
        db.add(new_wishlist)
        db.commit()
        
    return RedirectResponse(url="/wishlist", status_code=status.HTTP_302_FOUND)

@router.post("/remove/{wishlist_id}")
async def remove_from_wishlist(
    request: Request,
    wishlist_id: int,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
        
    wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id, Wishlist.user_id == user.id).first()
    if wishlist_item:
        db.delete(wishlist_item)
        db.commit()
        
    return RedirectResponse(url="/wishlist", status_code=status.HTTP_302_FOUND)
