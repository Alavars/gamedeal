import resend
from src.config import settings

resend.api_key = settings.resend_api_key

def send_price_drop_email(to_email: str, game_title: str, current_price: float, target_price: float):
    if not resend.api_key:
        print("Resend API key is missing. Skipping email sending.")
        return
        
    html_content = f"""
    <h2>Good News!</h2>
    <p>The price for <strong>{game_title}</strong> has dropped!</p>
    <p>Current Price: ${current_price}</p>
    <p>Your Target Price: ${target_price}</p>
    <br>
    <p>GameDealPulse Team</p>
    """
    
    try:
        r = resend.Emails.send({
            "from": settings.sender_email,
            "to": [to_email],
            "subject": f"Price Drop Alert: {game_title} is now ${current_price}!",
            "html": html_content
        })
        return r
    except Exception as e:
        print(f"Error sending email: {e}")
        return None
