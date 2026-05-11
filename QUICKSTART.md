# Restaurant Review & Feedback System - Quick Start

## Complete Local Setup (5 minutes)

### Prerequisites
- Python 3.8+
- Node.js 18+
- Supabase account
- Twilio WhatsApp account

### Step 1: Clone and Setup Backend

```bash
# Navigate to project root
cd lead-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials:
# - SUPABASE_URL
# - SUPABASE_KEY
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# - TWILIO_WHATSAPP_NUMBER
# - NEXTJS_URL (http://localhost:3000 for local)
```

### Step 2: Setup Database

```bash
# Run schema in Supabase SQL editor
# Copy contents of schema.sql and execute in Supabase

# Add a test restaurant (in Supabase SQL editor):
INSERT INTO restaurants (name, review_link)
VALUES ('Test Restaurant', 'https://g.page/r/YOUR_GOOGLE_REVIEW_LINK/review');
```

### Step 3: Setup Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local:
# FASTAPI_URL=http://localhost:8000
```

### Step 4: Start Both Services

**Terminal 1 - Backend:**
```bash
cd lead-generator
source venv/bin/activate
python main.py
```

Backend runs at: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd lead-generator/frontend
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Step 5: Test the Flow

1. **Get Restaurant ID from Supabase**
   - Open Supabase > Table Editor > restaurants
   - Copy the `id` (UUID) of your test restaurant

2. **Test Portal Page**
   ```
   http://localhost:3000/portal/[PASTE_RESTAURANT_ID_HERE]
   ```
   - Fill out the form
   - Submit and note the success message

3. **Get Customer ID**
   - Open Supabase > Table Editor > customers
   - Copy the `id` of the customer you just created

4. **Test Review Link**
   ```
   http://localhost:3000/review/[PASTE_CUSTOMER_ID_HERE]
   ```
   - Should redirect to Google Review
   - Check Supabase: `review_clicked` should be `true`

5. **Test Feedback Form**
   ```
   http://localhost:3000/feedback/[PASTE_CUSTOMER_ID_HERE]
   ```
   - Fill rating and improvement areas
   - Submit feedback
   - Check Supabase: feedback table should have new record

6. **Test Scheduler (Optional)**
   - Wait 2 hours after a checkin
   - Check logs for WhatsApp message sent
   - Or manually trigger by adjusting `created_at` in database

## Project Structure

```
lead-generator/
├── main.py                 # FastAPI server
├── models.py              # Pydantic models
├── database.py            # Supabase client
├── messaging.py           # Twilio WhatsApp
├── scheduler_jobs.py      # APScheduler jobs
├── config.py              # Environment config
├── requirements.txt       # Python dependencies
├── schema.sql            # Database schema
├── .env                  # Backend environment variables
│
└── frontend/
    ├── app/
    │   ├── portal/[rid]/      # WiFi portal
    │   ├── feedback/[cid]/    # Feedback form
    │   ├── review/[cid]/      # Review redirect
    │   ├── layout.tsx         # Root layout
    │   └── page.tsx           # Home page
    ├── components/
    │   ├── PortalForm.tsx     # Portal form client
    │   └── FeedbackForm.tsx   # Feedback form client
    ├── package.json
    ├── .env.local            # Frontend environment variables
    ├── README.md
    └── DEPLOYMENT.md
```

## API Endpoints

### Backend (FastAPI)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/restaurant/{rid}` | Get restaurant info |
| GET | `/customer/{cid}` | Get customer info |
| POST | `/checkin` | Save customer checkin |
| GET | `/review?cid={cid}` | Track review click & redirect |
| POST | `/feedback` | Save feedback |

### Frontend (NextJS)

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/portal/[rid]` | WiFi portal form |
| `/review/[cid]` | Review link redirect |
| `/feedback/[cid]` | Feedback form |

## Flow Overview

```
Customer connects to WiFi
    ↓
Router redirects to /portal/[rid]
    ↓
Customer fills form → Saved to DB
    ↓
2 hours later: Scheduler sends WhatsApp with /review/[cid] link
    ↓
Customer clicks → Logged in DB → Redirected to Google Review
    ↓
24 hours later (if no click): Scheduler sends WhatsApp with /feedback/[cid] link
    ↓
Customer fills feedback → Saved to DB
```

## Troubleshooting

### Backend won't start
- Check `.env` file exists and has all variables
- Verify Supabase credentials are correct
- Test Supabase connection: `python test_utils.py`

### Frontend won't start
- Run `npm install` again
- Delete `node_modules` and `.next`, reinstall
- Check `.env.local` has FASTAPI_URL

### Portal page shows 404
- Verify restaurant ID exists in Supabase
- Check backend is running on port 8000
- Check browser console for errors

### No WhatsApp messages
- Verify Twilio credentials in `.env`
- Check Twilio console for errors
- Verify phone number format: +1234567890
- Check backend logs for scheduler output

### Database errors
- Verify schema.sql was executed in Supabase
- Check Supabase service role key (not anon key)
- Test connection with Supabase dashboard

## Next Steps

1. **Test thoroughly locally**
2. **Deploy backend to Railway** (see DEPLOYMENT.md)
3. **Deploy frontend to Vercel** (see DEPLOYMENT.md)
4. **Configure GL.iNet router** with production URL
5. **Monitor and iterate**

## Support

- Backend docs: `API.md`
- Frontend docs: `frontend/README.md`
- Deployment guide: `frontend/DEPLOYMENT.md`
- Setup guide: `SETUP.md`

## Phase 2 (Future)

- Multi-restaurant support
- Restaurant owner dashboard
- Analytics and reporting
- Email notifications
- SMS fallback option
- Advanced feedback analytics
