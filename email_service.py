import resend
from config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Resend with API key
resend.api_key = settings.resend_api_key


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send an email using Resend.
    
    Args:
        to_email: Recipient's email address
        subject: Email subject line
        html_content: HTML content of the email
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        response = resend.Emails.send({
            "from": settings.resend_from_email,
            "to": to_email,
            "subject": subject,
            "html": html_content
        })
        
        logger.info(f"Email sent to {to_email}: {response}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


def create_review_request_email(customer_name: str, restaurant_name: str, review_link: str) -> tuple[str, str]:
    """
    Create a review request email.
    
    Args:
        customer_name: Customer's name
        restaurant_name: Restaurant name
        review_link: Link to track the review click
        
    Returns:
        tuple: (subject, html_content)
    """
    subject = f"How was your experience at {restaurant_name}? ⭐"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                padding: 40px;
                color: white;
                text-align: center;
            }}
            .content {{
                background: white;
                color: #333;
                border-radius: 8px;
                padding: 30px;
                margin-top: 20px;
            }}
            .button {{
                display: inline-block;
                background: #667eea;
                color: white;
                text-decoration: none;
                padding: 14px 32px;
                border-radius: 8px;
                font-weight: 600;
                margin: 20px 0;
                transition: background 0.3s;
            }}
            .button:hover {{
                background: #5568d3;
            }}
            .footer {{
                text-align: center;
                color: #666;
                font-size: 14px;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👋 Hi {customer_name}!</h1>
            <p style="font-size: 18px;">Thanks for visiting <strong>{restaurant_name}</strong></p>
        </div>
        
        <div class="content">
            <p>We hope you enjoyed your experience with us! 🎉</p>
            
            <p>Would you mind leaving us a quick review? It would mean the world to us and help other customers discover what makes us special.</p>
            
            <a href="{review_link}" class="button">⭐ Leave a Review</a>
            
            <p style="color: #666; font-size: 14px;">This will only take a minute, we promise!</p>
        </div>
        
        <div class="footer">
            <p>Thank you for your support! 🙏</p>
            <p style="font-size: 12px; color: #999;">
                If you have any concerns, please reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    
    return subject, html_content


def create_feedback_request_email(customer_name: str, restaurant_name: str, feedback_link: str) -> tuple[str, str]:
    """
    Create a feedback request email.
    
    Args:
        customer_name: Customer's name
        restaurant_name: Restaurant name
        feedback_link: Link to the feedback form
        
    Returns:
        tuple: (subject, html_content)
    """
    subject = f"Help us improve - Quick feedback for {restaurant_name} 💡"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 12px;
                padding: 40px;
                color: white;
                text-align: center;
            }}
            .content {{
                background: white;
                color: #333;
                border-radius: 8px;
                padding: 30px;
                margin-top: 20px;
            }}
            .button {{
                display: inline-block;
                background: #f5576c;
                color: white;
                text-decoration: none;
                padding: 14px 32px;
                border-radius: 8px;
                font-weight: 600;
                margin: 20px 0;
                transition: background 0.3s;
            }}
            .button:hover {{
                background: #e04456;
            }}
            .footer {{
                text-align: center;
                color: #666;
                font-size: 14px;
                margin-top: 30px;
            }}
            .badge {{
                display: inline-block;
                background: rgba(255, 255, 255, 0.2);
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 14px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👋 Hi {customer_name}!</h1>
            <p style="font-size: 18px;">Your feedback matters to us</p>
            <div class="badge">🔒 Private & Confidential</div>
        </div>
        
        <div class="content">
            <p>We noticed you haven't left a public review yet — and that's totally fine!</p>
            
            <p>Could you spare just <strong>1 minute</strong> to share some private feedback with us? It would really help {restaurant_name} improve.</p>
            
            <ul style="text-align: left; color: #666;">
                <li>✅ Quick & easy (5 questions max)</li>
                <li>✅ Completely private</li>
                <li>✅ Helps us serve you better</li>
            </ul>
            
            <a href="{feedback_link}" class="button">💬 Share Feedback</a>
            
            <p style="color: #666; font-size: 14px;">Your honest opinion helps us grow!</p>
        </div>
        
        <div class="footer">
            <p>Thank you for helping us improve! 🙏</p>
            <p style="font-size: 12px; color: #999;">
                Your feedback stays between us and will never be shared publicly.
            </p>
        </div>
    </body>
    </html>
    """
    
    return subject, html_content


def send_review_request_email(to_email: str, customer_name: str, restaurant_name: str, review_link: str) -> bool:
    """
    Send a review request email to a customer.
    
    Args:
        to_email: Customer's email address
        customer_name: Customer's name
        restaurant_name: Restaurant name
        review_link: Link to track the review click
        
    Returns:
        bool: True if email was sent successfully
    """
    subject, html_content = create_review_request_email(customer_name, restaurant_name, review_link)
    return send_email(to_email, subject, html_content)


def send_feedback_request_email(to_email: str, customer_name: str, restaurant_name: str, feedback_link: str) -> bool:
    """
    Send a feedback request email to a customer.
    
    Args:
        to_email: Customer's email address
        customer_name: Customer's name
        restaurant_name: Restaurant name
        feedback_link: Link to the feedback form
        
    Returns:
        bool: True if email was sent successfully
    """
    subject, html_content = create_feedback_request_email(customer_name, restaurant_name, feedback_link)
    return send_email(to_email, subject, html_content)
