import bcrypt
from typing import Optional
from fastapi import Request, HTTPException, status

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def extract_user_id_from_request(request: Request) -> Optional[int]:
    # 1. Cookie
    user_id = request.cookies.get("user_id")
    if user_id:
        try:
            return int(user_id)
        except ValueError:
            pass

    # 2. Authorization header: "Bearer <id>"
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        try:
            return int(token)
        except ValueError:
            pass

    # 3. Custom header: "X-User-Id"
    custom_header = request.headers.get("X-User-Id")
    if custom_header:
        try:
            return int(custom_header)
        except ValueError:
            pass

    return None

def get_current_user_id(request: Request) -> int:
    uid = extract_user_id_from_request(request)
    if uid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return uid

def get_optional_user_id(request: Request) -> Optional[int]:
    return extract_user_id_from_request(request)
