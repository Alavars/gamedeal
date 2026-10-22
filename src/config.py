import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DEFAULT_DB_FILE = os.path.join(DATA_DIR, "app.db").replace("\\", "/")

class Settings(BaseSettings):
    app_name: str = "GameDealPulse"
    app_env: str = "development"
    app_port: int = 8000
    secret_key: str = "supersecretkey"
    
    database_url: str = f"sqlite:///{DEFAULT_DB_FILE}"
    
    cheapshark_base_url: str = "https://www.cheapshark.com/api/1.0"
    
    resend_api_key: str = ""
    sender_email: str = "onboarding@resend.dev"

    class Config:
        env_file = ".env"

settings = Settings()
