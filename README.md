# Project: Restaurant Review & Feedback Automation System

## Overview
A backend system that captures WiFi login data from restaurant customers and:
1. Sends a WhatsApp/email message 2 hours after visit asking for a Google Review
2. If the customer does NOT click the review link within 24 hours, sends a follow-up internal feedback form to capture their neutral opinions

---

## Tech Stack
- **Backend:** Python + FastAPI
- **Database:** Supabase (PostgreSQL)
- **Task Scheduling:** APScheduler (inside FastAPI)
- **Messaging:** WhatsApp Business API via Twilio
- **Captive Portal:** GL.iNet router — portal page is a static HTML form that POSTs to FastAPI
- **Feedback Form:** Simple HTML page served by FastAPI

---

## System Flow

### Step 1 — Customer checks in
1. Customer connects to restaurant WiFi
2. Captive portal form appears
3. Customer enters Name + Phone number
4. Form POSTs to `POST /checkin` → saved in Supabase

### Step 2 — Review request (2 hours after checkin)
1. APScheduler job runs every 5 minutes
2. Finds customers where `message_sent = false` AND `created_at <= now() - 2 hours`
3. Sends WhatsApp: "Hey [Name], thanks for visiting [Restaurant]! Leave us a review: [yourapp.com/review?cid=xyz]"
4. Sets `message_sent = true`, `message_sent_at = now()`

### Step 3 — Click tracking
1. Customer clicks the review link
2. FastAPI endpoint `GET /review?cid=xyz` logs the click: sets `review_clicked = true`, `review_clicked_at = now()`
3. Immediately redirects customer to the real Google Review URL

### Step 4 — Feedback form fallback (24 hours after review message)
1. APScheduler job runs every 5 minutes
2. Finds customers where `message_sent = true` AND `review_clicked = false` AND `message_sent_at <= now() - 24 hours` AND `feedback_sent = false`
3. Sends WhatsApp: "Hey [Name], we noticed you haven't left a review yet — that's totally fine! Could you spare 1 minute to help us improve? [yourapp.com/feedback?cid=xyz]"
4. Sets `feedback_sent = true`

### Step 5 — Feedback form submission
1. Customer opens feedback form (simple HTML page)
2. Fills in: overall rating (1-5), improvement areas (food / service / speed / atmosphere / price), optional comment
3. Form POSTs to `POST /feedback` → saved in Supabase `feedback` table

---

## Supabase Tables

### `restaurants`
| Column       | Type  | Notes                     |
|--------------|-------|---------------------------|
| id           | uuid  | PK                        |
| name         | text  | restaurant name           |
| review_link  | text  | real Google Review URL    |

### `customers`
| Column            | Type        | Notes                          |
|-------------------|-------------|--------------------------------|
| id                | uuid (PK)   | used as cid in links           |
| name              | text        | from captive portal form       |
| phone             | text        | from captive portal form       |
| restaurant_id     | uuid (FK)   | references restaurants         |
| created_at        | timestamptz | checkin time, auto-generated   |
| message_sent      | boolean     | default false                  |
| message_sent_at   | timestamptz | when review request was sent   |
| review_clicked    | boolean     | default false                  |
| review_clicked_at | timestamptz | when review link was clicked   |
| feedback_sent     | boolean     | default false                  |

### `feedback`
| Column            | Type        | Notes                                              |
|-------------------|-------------|----------------------------------------------------|
| id                | uuid (PK)   | auto-generated                                     |
| customer_id       | uuid (FK)   | references customers                               |
| restaurant_id     | uuid (FK)   | references restaurants                             |
| rating            | int         | 1-5 stars                                          |
| improvement_areas | text[]      | array: food, service, speed, atmosphere, price     |
| comment           | text        | optional free text                                 |
| created_at        | timestamptz | auto-generated                                     |

---
## FastAPI Endpoints
- `POST /checkin` — receives customer data from captive portal, saves to Supabase
- `GET /review?cid={customer_id}` — logs review link click, redirects to Google Review URL
- `GET /feedback?cid={customer_id}` — serves the feedback HTML form
- `POST /feedback` — receives feedback form submission, saves to Supabase
- `GET /health` — health check

---

## APScheduler Jobs
### Job 1 — Send review request
- Every 5 minutes
- Query: `message_sent = false` AND `created_at <= now() - interval '2 hours'`
- Action: send WhatsApp with tracked review link, set `message_sent = true`, `message_sent_at = now()`

### Job 2 — Send feedback form
- Every 5 minutes
- Query: `message_sent = true` AND `review_clicked = false` AND `feedback_sent = false` AND `message_sent_at <= now() - interval '24 hours'`
- Action: send WhatsApp with feedback form link, set `feedback_sent = true`

---

## Environment Variables
- SUPABASE_URL
- SUPABASE_KEY
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_WHATSAPP_NUMBER
- BASE_URL (your server's public URL, used to build tracked links e.g. https://yourapp.com)

---

## Notes
- Start with one hardcoded restaurant for the pilot
- The captive portal form is a static HTML file served by the GL.iNet router
- The feedback form is a simple HTML page served directly by FastAPI
- No auth needed for MVP
- Keep it simple and working first, optimize later
