from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.connection import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    wishlist = relationship("Wishlist", back_populates="user")

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False) # CheapShark GameID
    title = Column(String, nullable=False)
    thumb_url = Column(String)
    
    wishlists = relationship("Wishlist", back_populates="game")

class Wishlist(Base):
    __tablename__ = "wishlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    target_price = Column(Float, nullable=True) # Send alert if price drops below this
    notify_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="wishlist")
    game = relationship("Game", back_populates="wishlists")
