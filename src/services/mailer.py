import resend
from src.config import settings

def send_price_drop_email(to_email: str, game_title: str, current_price: float, store_name: str, deal_url: str):
    resend.api_key = settings.resend_api_key

    if not settings.resend_api_key or "your_test_key_here" in settings.resend_api_key:
        print(f"Mock Email sent to {to_email}: {game_title} is now ${current_price} at {store_name}!")
        return {"success": True, "mock": True, "message": "Mock email logged to console"}

    html_content = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 500px; margin: 20px auto; padding: 25px; border: 1px solid #e5e7eb; border-radius: 12px; background-color: #ffffff;">
        <h2 style="color: #2563eb; margin-top: 0;">GameDealPulse Price Alert! 🎉</h2>
        <p style="color: #374151; font-size: 16px;">Great news! The game <strong>{game_title}</strong> from your wishlist is now on sale below your target price.</p>
        
        <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 15px; margin: 20px 0; text-align: center;">
            <span style="font-size: 14px; color: #15803d; font-weight: 600;">Current Best Price</span>
            <div style="font-size: 32px; font-weight: 800; color: #16a34a; margin-top: 4px;">${current_price}</div>
            <span style="font-size: 13px; color: #4b5563;">Available at: <strong>{store_name}</strong></span>
        </div>

        <div style="text-align: center; margin-top: 25px;">
            <a href="{deal_url}" target="_blank" style="display: inline-block; background-color: #2563eb; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 15px;">View Deal in Store</a>
        </div>

        <hr style="border: none; border-top: 1px solid #f3f4f6; margin: 30px 0 15px;" />
        <p style="font-size: 12px; color: #9ca3af; text-align: center; margin: 0;">
            You received this automated notification because {game_title} is tracked in your GameDealPulse wishlist.
        </p>
    </div>
    """

    try:
        params = {
            "from": settings.sender_email,
            "to": [to_email],
            "subject": f"Discount Alert: {game_title} is now ${current_price}!",
            "html": html_content
        }
        response = resend.Emails.send(params)
        print(f"Resend Email successfully sent to {to_email}: {response}")
        return {"success": True, "mock": False, "data": response}
    except Exception as e:
        error_msg = str(e)
        print(f"Failed to send email to {to_email}: {error_msg}")
        return {"success": False, "mock": False, "error": error_msg}
