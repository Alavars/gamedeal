from passlib.context import CryptContext
from typing import Optional
from fastapi import Request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_current_user_id(request: Request) -> Optional[int]:
    # We will use simple signed cookies or session middleware for auth
    # For now, let's assume session id is stored in cookie "session" 
    # Or just store user_id directly in cookie for this simple project (not secure in production without signing)
    try:
        user_id_str = request.cookies.get("user_id")
        if user_id_str:
            return int(user_id_str)
    except (ValueError, TypeError):
        pass
    return None
