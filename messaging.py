from twilio.rest import Client
from config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Twilio client
twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)


def send_whatsapp_message(to_phone: str, message: str) -> bool:
    """
    Send a WhatsApp message using Twilio.
    
    Args:
        to_phone: Recipient's phone number (must include country code)
        message: Message content to send
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        # Ensure phone number has country code
        if not to_phone.startswith('+'):
            to_phone = f'+{to_phone}'
        
        # Send message via Twilio WhatsApp
        message_response = twilio_client.messages.create(
            from_=settings.twilio_whatsapp_number,
            body=message,
            to=f'whatsapp:{to_phone}'
        )
        
        logger.info(f"WhatsApp message sent to {to_phone}: {message_response.sid}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message to {to_phone}: {str(e)}")
        return False


def create_review_request_message(customer_name: str, restaurant_name: str, review_link: str) -> str:
    """
    Create a review request message.
    
    Args:
        customer_name: Customer's name
        restaurant_name: Restaurant name
        review_link: Link to track the review click
        
    Returns:
        str: Formatted message
    """
    return (
        f"Hey {customer_name}! 👋\n\n"
        f"Thanks for visiting {restaurant_name}! We hope you enjoyed your experience.\n\n"
        f"Would you mind leaving us a quick review? It would mean the world to us! ⭐\n\n"
        f"{review_link}\n\n"
        f"Thank you! 🙏"
    )


def create_feedback_request_message(customer_name: str, restaurant_name: str, feedback_link: str) -> str:
    """
    Create a feedback request message.
    
    Args:
        customer_name: Customer's name
        restaurant_name: Restaurant name
        feedback_link: Link to the feedback form
        
    Returns:
        str: Formatted message
    """
    return (
        f"Hey {customer_name}! 👋\n\n"
        f"We noticed you haven't left a review yet — that's totally fine!\n\n"
        f"Could you spare just 1 minute to share some private feedback with {restaurant_name}? "
        f"It would really help us improve! 💡\n\n"
        f"{feedback_link}\n\n"
        f"Your feedback stays between us. Thank you! 🙏"
    )
