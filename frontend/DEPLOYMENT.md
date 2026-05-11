# Frontend Deployment Guide

## Local Development Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
Create `.env.local`:
```
FASTAPI_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Testing the Flow Locally

### 1. Start Backend (in separate terminal)
```bash
cd ..  # back to project root
python main.py
```

### 2. Test Portal Page
Navigate to: `http://localhost:3000/portal/[RESTAURANT_ID]`

Replace `[RESTAURANT_ID]` with an actual restaurant UUID from your Supabase database.

### 3. Test Feedback Page
Navigate to: `http://localhost:3000/feedback/[CUSTOMER_ID]`

Replace `[CUSTOMER_ID]` with an actual customer UUID from your Supabase database.

### 4. Test Review Redirect
Navigate to: `http://localhost:3000/review/[CUSTOMER_ID]`

This should log the click and redirect to the Google Review URL.

## Vercel Deployment

### Method 1: GitHub Integration (Recommended)

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "Import Project"
4. Select your repository
5. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
6. Add Environment Variable:
   - **Name**: `FASTAPI_URL`
   - **Value**: Your Railway/Render backend URL (e.g., `https://your-app.railway.app`)
7. Click "Deploy"

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Set environment variable
vercel env add FASTAPI_URL
# Enter your production backend URL when prompted

# Deploy to production
vercel --prod
```

## Backend Deployment (Railway)

### 1. Create Railway Account
Go to [railway.app](https://railway.app)

### 2. Deploy from GitHub

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python/FastAPI

### 3. Configure Environment Variables

In Railway dashboard, add:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
NEXTJS_URL=your_vercel_url
```

### 4. Configure Start Command

In Railway settings, set:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 5. Get Your Backend URL

Copy the Railway public URL (e.g., `https://your-app.railway.app`)

## Connecting Frontend and Backend

### After Both Are Deployed:

1. **Update Vercel Environment Variable**
   - Go to Vercel project settings
   - Update `FASTAPI_URL` to your Railway URL
   - Redeploy

2. **Update Railway Environment Variable**
   - Go to Railway project settings
   - Update `NEXTJS_URL` to your Vercel URL
   - Railway will auto-redeploy

## Domain Setup (Optional)

### Custom Domain for Frontend (Vercel)

1. Go to Vercel project settings > Domains
2. Add your custom domain (e.g., `portal.yourrestaurant.com`)
3. Update DNS records as instructed

### Custom Domain for Backend (Railway)

1. Go to Railway project settings > Domains
2. Add custom domain (e.g., `api.yourrestaurant.com`)
3. Update DNS records
4. Update `FASTAPI_URL` in Vercel

## Router Configuration

### GL.iNet Router Setup

1. Login to router admin panel
2. Go to WiFi Captive Portal settings
3. Set redirect URL to: `https://your-vercel-url.vercel.app/portal/[RESTAURANT_ID]`

Replace `[RESTAURANT_ID]` with the actual restaurant UUID.

## Testing Production Deployment

### 1. Portal Test
Visit: `https://your-vercel-url.vercel.app/portal/[RESTAURANT_ID]`
- Should show restaurant name
- Submit form should save to database
- Should show success message

### 2. Check Database
In Supabase, verify customer record was created.

### 3. Review Link Test
Visit: `https://your-vercel-url.vercel.app/review/[CUSTOMER_ID]`
- Should redirect to Google Review
- Customer record should show `review_clicked = true`

### 4. Feedback Form Test
Visit: `https://your-vercel-url.vercel.app/feedback/[CUSTOMER_ID]`
- Should show customer name and restaurant
- Submit feedback should save to database

### 5. Scheduler Test
Wait 2 hours after a checkin and verify WhatsApp messages are sent.

## Monitoring

### Vercel Logs
- Go to Vercel project > Deployments > [Latest] > Functions
- View real-time logs of server actions

### Railway Logs
- Go to Railway project > Deployments > [Latest]
- View FastAPI logs including scheduler jobs

### Supabase Logs
- Go to Supabase project > Logs
- Monitor database queries and errors

## Common Issues

### CORS Errors
Backend should not have CORS issues since all API calls are server-side.

### Environment Variables Not Loading
- Redeploy after changing environment variables
- Check that variable names match exactly
- Verify values don't have extra spaces

### 404 on Dynamic Routes
- Ensure restaurant/customer IDs are valid UUIDs
- Check Supabase for existing records

### Scheduler Not Running
- Check Railway logs for APScheduler output
- Verify cron jobs are registered on startup

## Production Checklist

- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] All environment variables configured
- [ ] Database connection working
- [ ] Test portal flow end-to-end
- [ ] Test review link redirect
- [ ] Test feedback form submission
- [ ] Verify WhatsApp messages send correctly
- [ ] Configure router captive portal
- [ ] Set up monitoring/alerts

## Security Notes

- FastAPI URL is never exposed to client browser
- All API calls happen server-side via Next.js Server Actions
- Environment variables are secure on both platforms
- Use HTTPS for all production URLs
