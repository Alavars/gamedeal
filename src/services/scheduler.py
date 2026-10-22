from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from src.database.connection import SessionLocal
from src.database.models import Wishlist
from src.services.cheapshark import cheapshark
from src.services.mailer import send_price_drop_email

scheduler = AsyncIOScheduler()

async def check_prices_job():
    print("Running background price check job...")
    db: Session = SessionLocal()
    try:
        # Get active wishlists
        active_items = db.query(Wishlist).filter(Wishlist.notify_active == True).all()
        if not active_items:
            return
            
        stores = await cheapshark.get_stores()
            
        for item in active_items:
            game_details = await cheapshark.get_game_details(item.game.external_id)
            if not game_details or 'deals' not in game_details:
                continue
                
            # Find the best deal
            deals = game_details['deals']
            if not deals:
                continue
                
            best_deal = min(deals, key=lambda d: float(d['price']))
            current_price = float(best_deal['price'])
            retail_price = float(best_deal['retailPrice'])
            
            should_notify = False
            
            if item.target_price is not None:
                # User set a specific target price
                if current_price <= item.target_price:
                    should_notify = True
            else:
                # User just wants any discount
                if current_price < retail_price:
                    should_notify = True
                    
            if should_notify:
                store_name = stores.get(best_deal['storeID'], "Unknown Store")
                deal_url = f"https://www.cheapshark.com/redirect?dealID={best_deal['dealID']}"
                
                # Send email
                send_price_drop_email(
                    to_email=item.user.email,
                    game_title=item.game.title,
                    current_price=current_price,
                    store_name=store_name,
                    deal_url=deal_url
                )
                
                # Disable notification so we don't spam
                item.notify_active = False
                db.commit()
                
    except Exception as e:
        print(f"Error in price check job: {e}")
    finally:
        db.close()

def start_scheduler():
    # Run every minute for testing, normally you'd do every 12-24 hours
    scheduler.add_job(check_prices_job, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started!")
