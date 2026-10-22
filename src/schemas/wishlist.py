from pydantic import BaseModel
from typing import Optional

class WishlistAddRequest(BaseModel):
    external_id: str
    title: str
    thumb_url: Optional[str] = ""
    target_price: Optional[float] = None

class WishlistUpdateRequest(BaseModel):
    target_price: Optional[float] = None
    notify_active: Optional[bool] = None

class GameInfo(BaseModel):
    id: int
    external_id: str
    title: str
    thumb_url: Optional[str] = None

    class Config:
        from_attributes = True

class WishlistItemResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    target_price: Optional[float] = None
    notify_active: bool
    game: Optional[GameInfo] = None

    class Config:
        from_attributes = True
