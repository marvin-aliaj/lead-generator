from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from typing import Optional
import logging

from config import settings
from database import supabase
from models import CheckinRequest, CheckinResponse, FeedbackRequest, FeedbackResponse
from messaging import send_whatsapp_message
from scheduler_jobs import send_review_requests, send_feedback_forms

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Restaurant Review & Feedback Automation System")

# Initialize APScheduler
scheduler = BackgroundScheduler()


@app.on_event("startup")
async def startup_event():
    """Start the scheduler when the app starts"""
    # Add scheduled jobs
    scheduler.add_job(
        send_review_requests,
        'interval',
        minutes=5,
        id='send_review_requests',
        replace_existing=True
    )
    scheduler.add_job(
        send_feedback_forms,
        'interval',
        minutes=5,
        id='send_feedback_forms',
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown the scheduler when the app stops"""
    scheduler.shutdown()
    logger.info("Scheduler shut down successfully")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/checkin", response_model=CheckinResponse)
async def checkin(request: CheckinRequest):
    """
    Receive customer data from captive portal and save to Supabase.
    Called when a customer connects to WiFi and submits the captive portal form.
    """
    try:
        # Insert customer data into Supabase
        result = supabase.table("customers").insert({
            "name": request.name,
            "phone": request.phone,
            "restaurant_id": request.restaurant_id,
        }).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to save customer data")

        customer_data = result.data[0]
        logger.info(f"Customer checked in: {customer_data['id']}")

        return CheckinResponse(
            id=customer_data["id"],
            name=customer_data["name"],
            phone=customer_data["phone"],
            restaurant_id=customer_data["restaurant_id"],
            created_at=customer_data["created_at"]
        )

    except Exception as e:
        logger.error(f"Error during checkin: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process checkin: {str(e)}")


@app.get("/review")
async def track_review_click(cid: str = Query(..., description="Customer ID")):
    """
    Track when a customer clicks the review link and redirect to Google Review.
    This logs the click and then redirects the user to the actual Google Review page.
    """
    try:
        # Get customer data to find the restaurant's review link
        customer_result = supabase.table("customers").select("*, restaurants(review_link)").eq("id", cid).execute()

        if not customer_result.data:
            raise HTTPException(status_code=404, detail="Customer not found")

        customer = customer_result.data[0]

        # Update customer record to log the click
        supabase.table("customers").update({
            "review_clicked": True,
            "review_clicked_at": datetime.now().isoformat()
        }).eq("id", cid).execute()

        logger.info(f"Review link clicked by customer: {cid}")

        # Redirect to the actual Google Review URL
        review_link = customer["restaurants"]["review_link"]
        return RedirectResponse(url=review_link)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking review click: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to track review click: {str(e)}")


@app.get("/feedback", response_class=HTMLResponse)
async def get_feedback_form(cid: str = Query(..., description="Customer ID")):
    """
    Serve the feedback form HTML page.
    Called when a customer clicks the feedback form link.
    """
    try:
        # Verify customer exists
        customer_result = supabase.table("customers").select("name, restaurant_id, restaurants(name)").eq("id", cid).execute()

        if not customer_result.data:
            return HTMLResponse(content="<h1>Invalid link</h1>", status_code=404)

        customer = customer_result.data[0]
        customer_name = customer["name"]
        restaurant_name = customer["restaurants"]["name"]

        # Read the feedback form HTML template
        with open("feedback_form.html", "r") as f:
            html_content = f.read()

        # Replace placeholders with actual data
        html_content = html_content.replace("{{customer_name}}", customer_name)
        html_content = html_content.replace("{{restaurant_name}}", restaurant_name)
        html_content = html_content.replace("{{customer_id}}", cid)

        return HTMLResponse(content=html_content)

    except FileNotFoundError:
        logger.error("feedback_form.html not found")
        raise HTTPException(status_code=500, detail="Feedback form template not found")
    except Exception as e:
        logger.error(f"Error serving feedback form: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load feedback form: {str(e)}")


@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Receive and save feedback form submission.
    Called when a customer submits the feedback form.
    """
    try:
        # Get customer data to find restaurant_id
        customer_result = supabase.table("customers").select("restaurant_id").eq("id", request.customer_id).execute()

        if not customer_result.data:
            raise HTTPException(status_code=404, detail="Customer not found")

        restaurant_id = customer_result.data[0]["restaurant_id"]

        # Validate rating
        if request.rating < 1 or request.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

        # Insert feedback into Supabase
        result = supabase.table("feedback").insert({
            "customer_id": request.customer_id,
            "restaurant_id": restaurant_id,
            "rating": request.rating,
            "improvement_areas": request.improvement_areas,
            "comment": request.comment
        }).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to save feedback")

        feedback_data = result.data[0]
        logger.info(f"Feedback received from customer: {request.customer_id}")

        return FeedbackResponse(
            id=feedback_data["id"],
            customer_id=feedback_data["customer_id"],
            restaurant_id=feedback_data["restaurant_id"],
            rating=feedback_data["rating"],
            improvement_areas=feedback_data["improvement_areas"],
            comment=feedback_data["comment"],
            created_at=feedback_data["created_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
