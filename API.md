# API Documentation

Base URL: `http://localhost:8000` (development) or your production URL

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-06T10:30:00.123456"
}
```

---

### 2. Customer Check-in

**POST** `/checkin`

Save customer information when they connect to WiFi via captive portal.

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "+1234567890",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "phone": "+1234567890",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-05-06T10:30:00.123456+00:00"
}
```

**Status Codes:**
- `200 OK` - Customer successfully checked in
- `500 Internal Server Error` - Failed to save customer data

**Example:**
```bash
curl -X POST http://localhost:8000/checkin \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "+1234567890",
    "restaurant_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

---

### 3. Track Review Click

**GET** `/review?cid={customer_id}`

Track when a customer clicks the review link and redirect them to Google Review page.

**Query Parameters:**
- `cid` (required) - Customer ID (UUID)

**Response:**
- Redirects to the restaurant's Google Review URL
- Updates customer record: `review_clicked = true`, `review_clicked_at = now()`

**Status Codes:**
- `302 Found` - Redirect to Google Review
- `404 Not Found` - Customer not found
- `500 Internal Server Error` - Failed to track click

**Example:**
```bash
# Opens in browser and redirects to Google Review
http://localhost:8000/review?cid=660e8400-e29b-41d4-a716-446655440000
```

---

### 4. Get Feedback Form

**GET** `/feedback?cid={customer_id}`

Serve the feedback form HTML page to the customer.

**Query Parameters:**
- `cid` (required) - Customer ID (UUID)

**Response:**
- HTML page with feedback form
- Form is pre-filled with customer name and restaurant name

**Status Codes:**
- `200 OK` - Feedback form HTML returned
- `404 Not Found` - Customer not found
- `500 Internal Server Error` - Template not found or error loading form

**Example:**
```bash
# Opens in browser
http://localhost:8000/feedback?cid=660e8400-e29b-41d4-a716-446655440000
```

---

### 5. Submit Feedback

**POST** `/feedback`

Receive and save customer feedback.

**Request Body:**
```json
{
  "customer_id": "660e8400-e29b-41d4-a716-446655440000",
  "rating": 4,
  "improvement_areas": ["food", "speed"],
  "comment": "Great food but service was a bit slow"
}
```

**Fields:**
- `customer_id` (required, string) - Customer UUID
- `rating` (required, integer) - Rating from 1 to 5
- `improvement_areas` (required, array of strings) - Areas to improve. Valid values: `food`, `service`, `speed`, `atmosphere`, `price`
- `comment` (optional, string) - Free text comment

**Response:**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "customer_id": "660e8400-e29b-41d4-a716-446655440000",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440000",
  "rating": 4,
  "improvement_areas": ["food", "speed"],
  "comment": "Great food but service was a bit slow",
  "created_at": "2026-05-06T10:30:00.123456+00:00"
}
```

**Status Codes:**
- `200 OK` - Feedback successfully saved
- `400 Bad Request` - Invalid rating (not between 1-5)
- `404 Not Found` - Customer not found
- `500 Internal Server Error` - Failed to save feedback

**Example:**
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "660e8400-e29b-41d4-a716-446655440000",
    "rating": 4,
    "improvement_areas": ["food", "speed"],
    "comment": "Great food but service was a bit slow"
  }'
```

---

## Scheduled Jobs

These jobs run automatically in the background via APScheduler.

### Job 1: Send Review Requests

**Frequency:** Every 5 minutes

**Logic:**
1. Find customers where:
   - `message_sent = false`
   - `created_at <= now() - 2 hours`
2. For each customer:
   - Send WhatsApp message with tracked review link: `{BASE_URL}/review?cid={customer_id}`
   - Update: `message_sent = true`, `message_sent_at = now()`

**Message Template:**
```
Hey {name}! 👋

Thanks for visiting {restaurant}! We hope you enjoyed your experience.

Would you mind leaving us a quick review? It would mean the world to us! ⭐

{review_link}

Thank you! 🙏
```

---

### Job 2: Send Feedback Forms

**Frequency:** Every 5 minutes

**Logic:**
1. Find customers where:
   - `message_sent = true`
   - `review_clicked = false`
   - `feedback_sent = false`
   - `message_sent_at <= now() - 24 hours`
2. For each customer:
   - Send WhatsApp message with feedback form link: `{BASE_URL}/feedback?cid={customer_id}`
   - Update: `feedback_sent = true`

**Message Template:**
```
Hey {name}! 👋

We noticed you haven't left a review yet — that's totally fine!

Could you spare just 1 minute to share some private feedback with {restaurant}? It would really help us improve! 💡

{feedback_link}

Your feedback stays between us. Thank you! 🙏
```

---

## Error Handling

All endpoints return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common error scenarios:
- Missing required fields → `400 Bad Request`
- Resource not found (customer, restaurant) → `404 Not Found`
- Database connection issues → `500 Internal Server Error`
- Twilio API errors → `500 Internal Server Error` (logged but doesn't stop the job)

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting in production using:
- FastAPI middleware (e.g., `slowapi`)
- Nginx rate limiting
- Cloudflare rate limiting

---

## Authentication

Currently no authentication is required (MVP). For production, consider:
- API keys for the captive portal endpoint
- Admin endpoints with JWT authentication
- IP whitelisting for internal services

---

## Testing with Postman/Insomnia

Import this collection or create requests manually:

1. **Health Check**: GET `{{base_url}}/health`
2. **Checkin**: POST `{{base_url}}/checkin` with JSON body
3. **Review Click**: GET `{{base_url}}/review?cid={{customer_id}}`
4. **Feedback Form**: GET `{{base_url}}/feedback?cid={{customer_id}}`
5. **Submit Feedback**: POST `{{base_url}}/feedback` with JSON body

Variables:
- `base_url`: http://localhost:8000
- `customer_id`: (get from checkin response)

---

## WebSocket Support

Not implemented in current version. Could be added for:
- Real-time feedback notifications
- Live dashboard updates
- Admin notifications

---

## API Versioning

Current version: v1 (implicit)

If you need versioning in the future:
```python
app = FastAPI(title="Restaurant Review API", version="1.0.0")

# Routes with version prefix
@app.post("/v1/checkin")
@app.post("/v2/checkin")
```

---

## CORS Configuration

To allow frontend apps from different domains:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## OpenAPI Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

These are available in development and should be disabled in production if needed.
