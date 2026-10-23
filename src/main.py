import os

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware

from src.config import settings
from src.database.connection import engine
from src.database.models import Base
from src.services.scheduler import start_scheduler
from src.routes import deals, auth, wishlist

# Create DB tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    pass

app = FastAPI(
    title=settings.app_name,
    description="REST API for GameDealPulse game tracking and price alerts",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware for React frontend (Vite/Create-React-App/Next)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_origin_regex=r"https?://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Mount React static assets if built
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
assets_dir = os.path.join(frontend_dist, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Include JSON API Routers
app.include_router(deals.router)
app.include_router(auth.router)
app.include_router(wishlist.router)

@app.get("/")
async def root(request: Request):
    index_file = os.path.join(frontend_dist, "index.html")
    # If React frontend is compiled, serve the full React Single Page Application!
    if os.path.exists(index_file):
        return FileResponse(index_file)

    return {
        "app": settings.app_name,
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": {
                "register": "POST /auth/register",
                "login": "POST /auth/login",
                "logout": "POST /auth/logout",
                "me": "GET /auth/me"
            },
            "deals": {
                "top": "GET /deals/top",
                "search": "GET /deals/search?query={title}",
                "details": "GET /deals/{game_id}"
            },
            "wishlist": {
                "list": "GET /wishlist",
                "add": "POST /wishlist/add",
                "remove": "DELETE /wishlist/{wishlist_id}",
                "update": "PUT /wishlist/{wishlist_id}",
                "test_email": "POST /wishlist/test-email"
            }
        }
    }

@app.get("/api")
async def api_info():
    return {
        "app": settings.app_name,
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "deals": "/deals",
            "wishlist": "/wishlist"
        }
    }

@app.get("/privacy")
async def privacy_api():
    return {
        "title": "Privacy Policy",
        "updated": "October 2026",
        "sections": [
            {
                "heading": "1. Information We Collect",
                "content": "At GameDealPulse, we respect your privacy and collect only the data necessary to provide our price tracking services. This includes: (a) Account Information: your email address and securely salted/hashed password; (b) Wishlist & Alerts: games you choose to track, custom target price thresholds, and notification statuses; (c) Technical Logs: minimal anonymized session logs strictly for security monitoring and error diagnosis."
            },
            {
                "heading": "2. How We Use Your Information",
                "content": "Your information is used exclusively to: (a) Deliver automated email notifications when games drop to or below your desired target price; (b) Maintain your personal wishlist and preferences across devices; (c) Authenticate your secure login sessions; (d) Prevent abusive API traffic and secure our server infrastructure."
            },
            {
                "heading": "3. Data Security & Storage",
                "content": "All sensitive credentials, including passwords, are hashed using industry-standard bcrypt encryption before being stored in our database. We never store plain-text passwords. Communications between your browser, our backend, and third-party APIs are encrypted using modern Transport Layer Security (TLS/HTTPS)."
            },
            {
                "heading": "4. Third-Party Services & Data Sharing",
                "content": "We do not sell, rent, monetize, or trade your personal information to advertisers or any third parties. We integrate with trusted third-party providers solely for operational purposes: (a) CheapShark API for fetching publicly available video game pricing data; (b) Resend API for delivering automated transactional price alert emails. Your email is provided to Resend solely for message delivery."
            },
            {
                "heading": "5. Cookies & Local Storage",
                "content": "We use essential cookies and browser local storage strictly for maintaining your authenticated user session. We do not use third-party tracking cookies or behavioral advertising trackers."
            },
            {
                "heading": "6. Your Rights & Data Deletion",
                "content": "You retain full control over your personal information. You have the right to request an export of your data or permanently delete your account and all associated wishlist records at any time by contacting our support team at support@gamedealpulse.com."
            }
        ]
    }

@app.get("/terms")
async def terms_api():
    return {
        "title": "Terms of Service",
        "updated": "October 2026",
        "sections": [
            {
                "heading": "1. Acceptance of Terms",
                "content": "By accessing, browsing, or registering an account on GameDealPulse, you acknowledge that you have read, understood, and agree to be bound by these Terms of Service. If you do not agree with any part of these terms, you must discontinue use of the platform immediately."
            },
            {
                "heading": "2. Description of the Service",
                "content": "GameDealPulse is an informational aggregator designed to help gamers track discounts across certified digital game storefronts. We provide price comparison data, historical discount analysis, and automated email alerts when games reach user-defined price thresholds."
            },
            {
                "heading": "3. Pricing Accuracy & Storefront Disclaimers",
                "content": "Prices, discounts, and deal availability are retrieved in real-time from external storefront APIs (including Steam, GOG, Epic Games Store, GreenManGaming, and Humble Bundle via CheapShark). While we strive for maximum accuracy, digital store prices fluctuate rapidly. GameDealPulse does not guarantee price availability. The final purchase price, taxes, currency conversion, and refund policies are governed solely by the merchant at checkout."
            },
            {
                "heading": "4. Affiliate & External Links",
                "content": "GameDealPulse may contain outbound referral links to third-party digital stores. Clicking a deal link redirects you to the respective merchant's platform. We are not responsible for the content, privacy practices, terms, or transactions conducted on third-party websites."
            },
            {
                "heading": "5. User Conduct & Prohibited Activities",
                "content": "You agree to use GameDealPulse for personal, non-commercial purposes. You may not: (a) Attempt to reverse engineer or breach the website security; (b) Execute automated scripts, scrapers, or flood requests that degrade service performance; (c) Create fraudulent accounts or use unauthorized email addresses for alert subscriptions."
            },
            {
                "heading": "6. Limitation of Liability",
                "content": "GameDealPulse is provided on an 'as-is' and 'as-available' basis without warranties of any kind. Under no circumstances shall GameDealPulse or its developers be held liable for direct, indirect, incidental, or consequential damages resulting from missed discounts, price changes, service interruptions, or third-party purchases."
            }
        ]
    }

@app.get("/contact")
async def contact_api():
    return {
        "title": "Support & Contact Us",
        "email": "support@gamedealpulse.com",
        "response_time": "Typically within 12–24 business hours",
        "office_hours": "Monday – Friday: 09:00 – 18:00 (UTC)",
        "faqs": [
            {
                "question": "How do price drop alerts work?",
                "answer": "When you add a game to your Wishlist, you can set a target price (for example, $15.00). Our background scheduler runs automated price checks. As soon as the price drops to or below your target, our system immediately sends an alert email with a direct link to the cheapest store."
            },
            {
                "question": "Which digital storefronts are tracked?",
                "answer": "We track over 30 legitimate, verified PC game storefronts through the CheapShark API, including Steam, Epic Games Store, GOG, Humble Store, GreenManGaming, Fanatical, GamersGate, and Gamesplanet."
            },
            {
                "question": "How frequently are game prices updated?",
                "answer": "Our automated background worker polls active storefront discounts every minute for tracked wishlist games and refreshes trending deals regularly."
            },
            {
                "question": "Is GameDealPulse completely free?",
                "answer": "Yes! Searching for deals, tracking price history, and receiving automated price drop notifications is 100% free for all registered users."
            },
            {
                "question": "Why didn't I receive an email alert?",
                "answer": "Check your Spam or Promotions folder and ensure your target price is realistic. You can also click the 'Test Email' button in your navigation bar to confirm your email delivery is operating correctly."
            },
            {
                "question": "How do I delete my account or stop emails?",
                "answer": "You can remove individual games from your Wishlist anytime to stop alerts for those titles, or contact us at support@gamedealpulse.com for complete account deletion."
            }
        ]
    }
