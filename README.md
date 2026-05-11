# Restaurant Review & Feedback Automation System

A complete system that captures customer data via WiFi portal and automates review requests and feedback collection through WhatsApp.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Documentation](#documentation)
- [System Flow](#system-flow)
- [Project Structure](#project-structure)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Supabase account
- Twilio WhatsApp Business account

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Setup database (run schema.sql in Supabase)

# Start backend
python main.py
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with backend URL

# Start frontend
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Detailed Setup

See **[QUICKSTART.md](QUICKSTART.md)** for complete step-by-step instructions.

---

## 📖 Project Overview

A system that:
1. **Captures** customer data via WiFi login portal
2. **Sends** WhatsApp message 2 hours after visit asking for Google Review
3. **Tracks** if customer clicks the review link
4. **Follows up** with feedback form if no review click within 24 hours
5. **Collects** structured feedback for internal improvement

### Key Features
- ✅ Mobile-first WiFi portal
- ✅ Automated WhatsApp messaging via Twilio
- ✅ Review link click tracking
- ✅ Beautiful feedback form with star ratings
- ✅ Scheduler-based automation (APScheduler)
- ✅ Secure server-side API communication
- ✅ Ready for production deployment

---

## 🛠 Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database:** Supabase (PostgreSQL)
- **Scheduler:** APScheduler
- **Messaging:** Twilio WhatsApp API
- **Hosting:** Railway / Render

### Frontend
- **Framework:** Next.js 16 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Hosting:** Vercel

### Infrastructure
- **Router:** GL.iNet (Captive Portal)
- **Architecture:** Server-side API calls (FastAPI URL never exposed)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | Complete local setup guide (5 minutes) |
| **[SETUP.md](SETUP.md)** | Backend setup and configuration |
| **[API.md](API.md)** | API endpoint documentation |
| **[frontend/README.md](frontend/README.md)** | Frontend documentation |
| **[frontend/DEPLOYMENT.md](frontend/DEPLOYMENT.md)** | Deployment guide for Vercel & Railway |
| **[frontend/IMPLEMENTATION.md](frontend/IMPLEMENTATION.md)** | Implementation details and features |

---

## 🔄 System Flow

```
Customer connects to WiFi
    ↓
Portal: /portal/[restaurant-id]
Customer enters name + phone
    ↓
Data saved to Supabase
    ↓
⏰ 2 hours later
Scheduler sends WhatsApp with review link
    ↓
Customer clicks: /review/[customer-id]
Logs click → Redirects to Google Review
    ↓
⏰ 24 hours after message (if no click)
Scheduler sends WhatsApp with feedback link
    ↓
Customer fills feedback: /feedback/[customer-id]
Rating + improvement areas saved
    ↓
✅ Complete!
```

---

## 📁 Project Structure

```
lead-generator/
│
├── main.py                    # FastAPI application
├── models.py                  # Pydantic models
├── database.py                # Supabase client
├── messaging.py               # Twilio WhatsApp integration
├── scheduler_jobs.py          # APScheduler automation
├── config.py                  # Environment configuration
├── schema.sql                 # Database schema
├── requirements.txt           # Python dependencies
├── .env                       # Backend environment variables
│
├── QUICKSTART.md             # Quick start guide
├── SETUP.md                  # Backend setup guide
├── API.md                    # API documentation
├── README.md                 # This file
│
└── frontend/                 # Next.js frontend
    ├── app/
    │   ├── portal/[rid]/     # WiFi portal page
    │   │   ├── page.tsx
    │   │   └── actions.ts
    │   ├── review/[cid]/     # Review redirect page
    │   │   ├── page.tsx
    │   │   └── actions.ts
    │   ├── feedback/[cid]/   # Feedback form page
    │   │   ├── page.tsx
    │   │   └── actions.ts
    │   ├── layout.tsx
    │   ├── page.tsx
    │   └── globals.css
    │
    ├── components/
    │   ├── PortalForm.tsx    # Portal form component
    │   └── FeedbackForm.tsx  # Feedback form component
    │
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── next.config.ts
    ├── .env.local            # Frontend environment variables
    │
    ├── README.md             # Frontend docs
    ├── DEPLOYMENT.md         # Deployment guide
    └── IMPLEMENTATION.md     # Implementation details
```

---

## 🗄 Database Schema

### Tables

**restaurants**
- `id` (uuid, PK)
- `name` (text)
- `review_link` (text) - Google Review URL

**customers**
- `id` (uuid, PK)
- `name` (text)
- `phone` (text)
- `restaurant_id` (uuid, FK)
- `created_at` (timestamptz)
- `message_sent` (boolean)
- `message_sent_at` (timestamptz)
- `review_clicked` (boolean)
- `review_clicked_at` (timestamptz)
- `feedback_sent` (boolean)

**feedback**
- `id` (uuid, PK)
- `customer_id` (uuid, FK)
- `restaurant_id` (uuid, FK)
- `rating` (int, 1-5)
- `improvement_areas` (text[])
- `comment` (text)
- `created_at` (timestamptz)

See `schema.sql` for complete DDL.

---

## 🔌 API Endpoints

### Backend (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/restaurant/{rid}` | Get restaurant info |
| GET | `/customer/{cid}` | Get customer info |
| POST | `/checkin` | Save customer checkin |
| GET | `/review?cid={cid}` | Track click & redirect |
| POST | `/feedback` | Save feedback |

### Frontend (Next.js)

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/portal/[rid]` | WiFi portal form |
| `/review/[cid]` | Review link redirect |
| `/feedback/[cid]` | Feedback form |

---

## ⏰ Automated Jobs

### Job 1: Send Review Requests
- **Runs:** Every 5 minutes
- **Finds:** Customers where `message_sent = false` AND `created_at <= now() - 2 hours`
- **Action:** Send WhatsApp with review link

### Job 2: Send Feedback Forms
- **Runs:** Every 5 minutes
- **Finds:** Customers where `message_sent = true` AND `review_clicked = false` AND `feedback_sent = false` AND `message_sent_at <= now() - 24 hours`
- **Action:** Send WhatsApp with feedback link

---

## 🔐 Environment Variables

### Backend (.env)
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
NEXTJS_URL=http://localhost:3000
```

### Frontend (.env.local)
```
FASTAPI_URL=http://localhost:8000
```

---

## 🚀 Deployment

### Quick Deploy

1. **Backend to Railway**
   - Connect GitHub repo
   - Add environment variables
   - Deploy automatically

2. **Frontend to Vercel**
   - Connect GitHub repo
   - Set root directory to `frontend`
   - Add `FASTAPI_URL` environment variable
   - Deploy automatically

See **[frontend/DEPLOYMENT.md](frontend/DEPLOYMENT.md)** for detailed instructions.

---

## 🧪 Testing

### Test Locally

1. Start backend: `python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Get restaurant ID from Supabase
4. Visit: `http://localhost:3000/portal/[restaurant-id]`
5. Fill form and submit
6. Check Supabase for customer record
7. Test review link: `http://localhost:3000/review/[customer-id]`
8. Test feedback form: `http://localhost:3000/feedback/[customer-id]`

### Test Production

Follow the same flow but use your deployed URLs.

---

## 🎯 Phase 2 Features (Future)

- Multi-restaurant dashboard
- Restaurant owner login/CRM
- Advanced analytics
- Email notifications
- SMS fallback
- Custom branding per restaurant
- Automated reporting

---

## 📧 Support

For issues or questions:
1. Check documentation in the relevant `.md` files
2. Review API docs in `API.md`
3. Check deployment guide in `frontend/DEPLOYMENT.md`

---

## 📄 License

Proprietary - All rights reserved

---

## ✅ Status

**Phase 1 Complete:**
- ✅ Backend fully implemented
- ✅ Frontend fully implemented
- ✅ Database schema complete
- ✅ Scheduler working
- ✅ WhatsApp integration
- ✅ Mobile-optimized UI
- ✅ Ready for deployment

**Next Steps:**
1. Deploy to production (Railway + Vercel)
2. Configure GL.iNet router
3. Test end-to-end flow
4. Monitor and iterate
