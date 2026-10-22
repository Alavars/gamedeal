from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.database.models import User, Game, Wishlist
from src.schemas.wishlist import (
    WishlistAddRequest,
    WishlistUpdateRequest,
    WishlistItemResponse,
)
from src.utils.security import get_current_user_id

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.get("", response_model=List[WishlistItemResponse])
@router.get("/", response_model=List[WishlistItemResponse])
async def get_wishlist(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    return items

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_to_wishlist(
    payload: WishlistAddRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Ensure game exists in database
    game = db.query(Game).filter(Game.external_id == payload.external_id).first()
    if not game:
        game = Game(
            external_id=payload.external_id,
            title=payload.title,
            thumb_url=payload.thumb_url or ""
        )
        db.add(game)
        db.commit()
        db.refresh(game)
    else:
        # Update thumbnail or title if empty or changed
        if payload.thumb_url and not game.thumb_url:
            game.thumb_url = payload.thumb_url
            db.commit()

    # Check if already in wishlist
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.game_id == game.id
    ).first()

    if existing:
        if payload.target_price is not None:
            existing.target_price = payload.target_price
            db.commit()
            db.refresh(existing)
        return {
            "message": "Game is already in your wishlist",
            "item_id": existing.id,
            "game_id": game.id,
            "already_existed": True
        }

    # Create new wishlist entry
    new_wishlist = Wishlist(
        user_id=user_id,
        game_id=game.id,
        target_price=payload.target_price,
        notify_active=True
    )
    db.add(new_wishlist)
    db.commit()
    db.refresh(new_wishlist)

    return {
        "message": "Game added to wishlist",
        "item_id": new_wishlist.id,
        "game_id": game.id,
        "already_existed": False
    }

@router.delete("/{wishlist_id}")
@router.post("/remove/{wishlist_id}")
async def remove_from_wishlist(
    wishlist_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    item = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found"
        )

    db.delete(item)
    db.commit()

    return {"message": "Game removed from wishlist", "wishlist_id": wishlist_id}

@router.put("/{wishlist_id}")
async def update_wishlist_item(
    wishlist_id: int,
    payload: WishlistUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    item = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == user_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found"
        )

    if payload.target_price is not None:
        item.target_price = payload.target_price
    if payload.notify_active is not None:
        item.notify_active = payload.notify_active

    db.commit()
    db.refresh(item)

    return {
        "message": "Wishlist item updated",
        "item": {
            "id": item.id,
            "target_price": item.target_price,
            "notify_active": item.notify_active
        }
    }

@router.post("/test-email")
@router.get("/test-email")
async def send_test_email(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    from src.services.mailer import send_price_drop_email
    result = send_price_drop_email(
        to_email=user.email,
        game_title="GameDealPulse Setup Test",
        current_price=9.99,
        store_name="Steam",
        deal_url="https://www.cheapshark.com"
    )
    if not result.get("success"):
        return {
            "status": "error",
            "message": f"Resend error: {result.get('error')}"
        }
    return {
        "status": "success",
        "message": f"Test email sent to {user.email}! Check your inbox (or spam folder)."
    }
