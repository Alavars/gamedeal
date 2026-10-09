from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.database.connection import SessionLocal
from src.database.models import Wishlist, Game, User
from src.services.cheapshark import cheapshark
from src.services.mailer import send_price_drop_email

scheduler = AsyncIOScheduler()

async def check_prices_and_notify():
    print("Running background price check...")
    db = SessionLocal()
    try:
        wishlists = db.query(Wishlist).filter(Wishlist.notify_active == True).all()
        for item in wishlists:
            try:
                game_details = await cheapshark.get_game_details(item.game.external_id)
                if not game_details or 'deals' not in game_details or len(game_details['deals']) == 0:
                    continue
                    
                cheapest_deal = min(game_details['deals'], key=lambda x: float(x['price']))
                current_price = float(cheapest_deal['price'])
                
                if item.target_price and current_price <= item.target_price:
                    print(f"Price dropped for {item.game.title} to {current_price}! Sending email to {item.user.email}")
                    send_price_drop_email(
                        to_email=item.user.email,
                        game_title=item.game.title,
                        current_price=current_price,
                        target_price=item.target_price
                    )
                    
                    # Deactivate notification to prevent spamming the user every check
                    item.notify_active = False
                    db.commit()
            except Exception as e:
                print(f"Error checking price for game {item.game.title}: {e}")
    finally:
        db.close()

def start_scheduler():
    # In a real app we might run this every few hours, let's run every minute for easy testing during development
    scheduler.add_job(check_prices_and_notify, 'interval', minutes=5)
    scheduler.start()
