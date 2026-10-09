from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    wishlists = relationship("Wishlist", back_populates="user")

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    thumb_url = Column(String)
    steam_rating = Column(String)

    wishlists = relationship("Wishlist", back_populates="game")
    price_history = relationship("PriceHistory", back_populates="game")

class Wishlist(Base):
    __tablename__ = 'wishlists'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    target_price = Column(Float, nullable=True)
    notify_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="wishlists")
    game = relationship("Game", back_populates="wishlists")

class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    store_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    game = relationship("Game", back_populates="price_history")
