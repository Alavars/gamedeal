from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.database.models import User
from src.utils.security import get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.post("/login")
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "auth/login.html", 
            {"request": request, "error": "Invalid email or password"}
        )
    
    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@router.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/register")
async def register_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            "auth/register.html", 
            {"request": request, "error": "Email already registered"}
        )
    
    hashed_password = get_password_hash(password)
    new_user = User(email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    request.session["user_id"] = new_user.id
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
