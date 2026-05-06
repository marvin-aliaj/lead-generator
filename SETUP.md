# Setup Guide

## Prerequisites
- Python 3.9 or higher
- Supabase account
- Twilio account with WhatsApp Business API access
- GL.iNet router (for captive portal)

## Step 1: Clone and Install Dependencies

```bash
cd lead-generator
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Set Up Supabase

1. Create a new Supabase project at https://supabase.com
2. Go to the SQL Editor in your Supabase dashboard
3. Copy and paste the contents of `schema.sql` and execute it
4. Note your project URL and anon key from Settings > API

### Update the Default Restaurant

After running the schema, update the default restaurant's Google Review link:

```sql
UPDATE restaurants 
SET review_link = 'https://g.page/r/YOUR_ACTUAL_GOOGLE_REVIEW_LINK/review'
WHERE name = 'Demo Restaurant';
```

Get your Google Review link:
1. Go to your Google Business Profile
2. Click "Get more reviews"
3. Copy the short link provided

## Step 3: Set Up Twilio WhatsApp

1. Create a Twilio account at https://www.twilio.com
2. Set up WhatsApp Business API:
   - Go to Messaging > Try it out > Send a WhatsApp message
   - Follow the instructions to connect WhatsApp Sandbox (for testing)
   - For production, apply for WhatsApp Business API approval
3. Note your:
   - Account SID
   - Auth Token
   - WhatsApp number (format: `whatsapp:+14155238886`)

## Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
BASE_URL=http://localhost:8000  # Change to your public URL in production
```

## Step 5: Get Restaurant ID

After setting up Supabase, get your restaurant ID:

```bash
# Option 1: Check in Supabase dashboard (Table Editor > restaurants)
# Option 2: Query via API
python -c "from database import supabase; print(supabase.table('restaurants').select('id, name').execute())"
```

Copy the restaurant ID for the next step.

## Step 6: Configure Captive Portal

1. Open `captive_portal.html`
2. Replace `YOUR_RESTAURANT_ID_HERE` with your actual restaurant ID
3. Replace `YOUR_API_URL` with your FastAPI server URL
4. Upload this file to your GL.iNet router's captive portal configuration

### GL.iNet Router Setup:
1. Access router admin panel (usually http://192.168.8.1)
2. Go to Applications > Captive Portal
3. Enable captive portal
4. Upload the modified `captive_portal.html`

## Step 7: Run the Application

### Development Mode
```bash
python main.py
```

The server will start at http://localhost:8000

### Production Mode

1. Install a production ASGI server (already in requirements.txt):
```bash
pip install uvicorn[standard]
```

2. Run with proper configuration:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

Note: Use only 1 worker to avoid APScheduler running multiple times.

### Using a Process Manager (Recommended)

Install and configure a process manager like systemd or supervisor.

Example systemd service file (`/etc/systemd/system/restaurant-review.service`):

```ini
[Unit]
Description=Restaurant Review & Feedback System
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/lead-generator
Environment="PATH=/path/to/lead-generator/venv/bin"
ExecStart=/path/to/lead-generator/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable restaurant-review
sudo systemctl start restaurant-review
```

## Step 8: Deploy to Production

### Option 1: Deploy to a VPS (DigitalOcean, Linode, AWS EC2)

1. Set up a server with Python 3.9+
2. Install nginx as reverse proxy
3. Use systemd to manage the service
4. Configure SSL with Let's Encrypt
5. Update `BASE_URL` in `.env` to your public domain

### Option 2: Deploy to Render.com

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
5. Add environment variables in Render dashboard
6. Update `BASE_URL` to your Render URL

### Option 3: Deploy to Railway.app

1. Create a new project on Railway
2. Connect your GitHub repository
3. Railway will auto-detect the Python app
4. Add environment variables
5. Update `BASE_URL` to your Railway URL

## Step 9: Test the System

### Test Checkin Endpoint
```bash
curl -X POST http://localhost:8000/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "+1234567890",
    "restaurant_id": "YOUR_RESTAURANT_ID"
  }'
```

### Test Review Click Tracking
Open in browser:
```
http://localhost:8000/review?cid=CUSTOMER_ID_FROM_CHECKIN
```

### Test Feedback Form
Open in browser:
```
http://localhost:8000/feedback?cid=CUSTOMER_ID_FROM_CHECKIN
```

### Test Scheduled Jobs

To test the scheduled jobs without waiting, you can manually trigger them:

```python
from scheduler_jobs import send_review_requests, send_feedback_forms

# Modify the cutoff time in scheduler_jobs.py temporarily
# Change: cutoff_time = datetime.now() - timedelta(hours=2)
# To: cutoff_time = datetime.now() + timedelta(hours=1)

send_review_requests()
send_feedback_forms()
```

## Monitoring and Logs

The application logs important events. View logs:

```bash
# If using systemd
sudo journalctl -u restaurant-review -f

# If running directly
# Logs appear in console output
```

## Troubleshooting

### Messages Not Sending
- Check Twilio credentials
- Verify WhatsApp Sandbox is active (for testing)
- Check phone number format (must include country code with +)
- Review Twilio console for error messages

### Database Errors
- Verify Supabase credentials
- Check that tables exist (run schema.sql)
- Ensure restaurant_id is valid

### Scheduler Not Running
- Verify app is running with only 1 worker
- Check logs for scheduler startup message
- Restart the application

### Review Link Not Redirecting
- Verify restaurant's review_link is correct in database
- Check that customer ID is valid

## Security Notes

- Keep `.env` file secure and never commit it to version control
- In production, consider adding rate limiting
- Add authentication if you need admin endpoints
- Use HTTPS in production
- Regularly rotate Twilio credentials
- Monitor for suspicious activity in Supabase dashboard

## Next Steps

- Customize message templates in `messaging.py`
- Adjust timing (2 hours, 24 hours) in `scheduler_jobs.py`
- Add email notifications alongside WhatsApp
- Create an admin dashboard to view feedback
- Add analytics and reporting
- Implement A/B testing for messages
