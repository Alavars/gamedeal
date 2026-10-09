from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings
import os

db_path = settings.database_url.replace("sqlite:///", "")
# Create directory if it doesn't exist
os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
