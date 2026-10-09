from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from src.config import settings
from src.database.connection import engine
from src.database.models import Base

# Create DB tables
Base.metadata.create_all(bind=engine)

from contextlib import asynccontextmanager
from src.services.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    pass

app = FastAPI(title=settings.app_name, lifespan=lifespan)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include Routers
from src.routes import deals, auth, wishlist
app.include_router(deals.router)
app.include_router(auth.router)
app.include_router(wishlist.router)

from src.routes.wishlist import get_current_user
from src.database.connection import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"app_name": settings.app_name, "user": user}
    )
