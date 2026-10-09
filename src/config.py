from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "GameDealPulse"
    app_env: str = "development"
    app_port: int = 8000
    secret_key: str = "supersecretkey"
    
    database_url: str = "sqlite:///./data/app.db"
    
    cheapshark_base_url: str = "https://www.cheapshark.com/api/1.0"
    
    resend_api_key: str = ""
    sender_email: str = "onboarding@resend.dev"

    class Config:
        env_file = ".env"

settings = Settings()
