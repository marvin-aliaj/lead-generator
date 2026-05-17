from datetime import datetime, timedelta
import logging

from database import supabase
from messaging import send_whatsapp_message, create_review_request_message, create_feedback_request_message
from email_service import send_review_request_email, send_feedback_request_email
from config import settings

logger = logging.getLogger(__name__)


def send_review_requests():
    """
    Scheduled job that runs every 5 minutes.
    Finds customers who checked in 2+ hours ago and haven't received a review request yet.
    Sends them a WhatsApp message and/or email with a tracked review link.
    """
    try:
        # Calculate the cutoff time (2 hours ago)
        cutoff_time = datetime.now() - timedelta(hours=2)
        
        # Query customers who need a review request
        result = supabase.table("customers")\
            .select("*, restaurants(name, review_link)")\
            .eq("message_sent", False)\
            .lte("created_at", cutoff_time.isoformat())\
            .execute()
        
        customers = result.data
        
        if not customers:
            logger.info("No customers found for review requests")
            return
        
        logger.info(f"Found {len(customers)} customers for review requests")
        
        # Process each customer
        for customer in customers:
            try:
                customer_id = customer["id"]
                customer_name = customer["name"]
                customer_phone = customer["phone"]
                customer_email = customer.get("email")
                restaurant_name = customer["restaurants"]["name"]
                
                # Create tracked review link
                review_link = f"{settings.base_url}/review/{customer_id}"
                
                # Send WhatsApp message
                whatsapp_message = create_review_request_message(
                    customer_name=customer_name,
                    restaurant_name=restaurant_name,
                    review_link=review_link
                )
                whatsapp_success = send_whatsapp_message(customer_phone, whatsapp_message)
                
                # Send email if email address is provided
                email_success = False
                if customer_email:
                    email_success = send_review_request_email(
                        to_email=customer_email,
                        customer_name=customer_name,
                        restaurant_name=restaurant_name,
                        review_link=review_link
                    )
                
                # Update customer record if at least one method succeeded
                if whatsapp_success or email_success:
                    supabase.table("customers").update({
                        "message_sent": True,
                        "message_sent_at": datetime.now().isoformat()
                    }).eq("id", customer_id).execute()
                    
                    channels = []
                    if whatsapp_success:
                        channels.append("WhatsApp")
                    if email_success:
                        channels.append("Email")
                    
                    logger.info(f"Review request sent to customer {customer_id} via {', '.join(channels)}")
                else:
                    logger.error(f"Failed to send review request to customer {customer_id} via any channel")
                    
            except Exception as e:
                logger.error(f"Error processing customer {customer.get('id', 'unknown')}: {str(e)}")
                continue
        
        logger.info(f"Review request job completed. Processed {len(customers)} customers")
        
    except Exception as e:
        logger.error(f"Error in send_review_requests job: {str(e)}")


def send_feedback_forms():
    """
    Scheduled job that runs every 5 minutes.
    Finds customers who:
    - Received a review request 24+ hours ago
    - Haven't clicked the review link
    - Haven't received a feedback request yet
    Sends them a WhatsApp message and/or email with a feedback form link.
    """
    try:
        # Calculate the cutoff time (24 hours ago)
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        # Query customers who need a feedback form
        result = supabase.table("customers")\
            .select("*, restaurants(name)")\
            .eq("message_sent", True)\
            .eq("review_clicked", False)\
            .eq("feedback_sent", False)\
            .lte("message_sent_at", cutoff_time.isoformat())\
            .execute()
        
        customers = result.data
        
        if not customers:
            logger.info("No customers found for feedback forms")
            return
        
        logger.info(f"Found {len(customers)} customers for feedback forms")
        
        # Process each customer
        for customer in customers:
            try:
                customer_id = customer["id"]
                customer_name = customer["name"]
                customer_phone = customer["phone"]
                customer_email = customer.get("email")
                restaurant_name = customer["restaurants"]["name"]
                
                # Create feedback form link
                feedback_link = f"{settings.base_url}/feedback/{customer_id}"
                
                # Send WhatsApp message
                whatsapp_message = create_feedback_request_message(
                    customer_name=customer_name,
                    restaurant_name=restaurant_name,
                    feedback_link=feedback_link
                )
                whatsapp_success = send_whatsapp_message(customer_phone, whatsapp_message)
                
                # Send email if email address is provided
                email_success = False
                if customer_email:
                    email_success = send_feedback_request_email(
                        to_email=customer_email,
                        customer_name=customer_name,
                        restaurant_name=restaurant_name,
                        feedback_link=feedback_link
                    )
                
                # Update customer record if at least one method succeeded
                if whatsapp_success or email_success:
                    supabase.table("customers").update({
                        "feedback_sent": True
                    }).eq("id", customer_id).execute()
                    
                    channels = []
                    if whatsapp_success:
                        channels.append("WhatsApp")
                    if email_success:
                        channels.append("Email")
                    
                    logger.info(f"Feedback form sent to customer {customer_id} via {', '.join(channels)}")
                else:
                    logger.error(f"Failed to send feedback form to customer {customer_id} via any channel")
                    
            except Exception as e:
                logger.error(f"Error processing customer {customer.get('id', 'unknown')}: {str(e)}")
                continue
        
        logger.info(f"Feedback form job completed. Processed {len(customers)} customers")
        
    except Exception as e:
        logger.error(f"Error in send_feedback_forms job: {str(e)}")
