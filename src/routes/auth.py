from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.database.models import User
from src.schemas.user import UserCreate, UserLogin, UserResponse
from src.utils.security import get_password_hash, verify_password, get_current_user_id

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    new_user = User(email=payload.email, password_hash=get_password_hash(payload.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email
        }
    }

@router.post("/login")
async def login(payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Set cookie for session / browser support
    response.set_cookie(
        key="user_id",
        value=str(user.id),
        httponly=True,
        samesite="lax",
        path="/"
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email
        },
        "token": str(user.id)
    }

@router.post("/logout")
@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="user_id", path="/")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
