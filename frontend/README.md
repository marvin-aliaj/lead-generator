# Restaurant Review & Feedback System - Frontend

This is the NextJS frontend for the Restaurant Review & Feedback Automation System.

## Tech Stack

- **Next.js 16** (App Router)
- **React 19**
- **TypeScript**
- **Tailwind CSS**
- **Server Actions** for backend communication

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend FastAPI server running (see main project README)

### Installation

```bash
npm install
```

### Environment Variables

Create a `.env.local` file:

```
FASTAPI_URL=http://localhost:8000
```

For production deployment on Vercel, set this to your Railway/Render backend URL.

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build

```bash
npm run build
npm start
```

## Project Structure

```
app/
├── portal/[rid]/          # WiFi portal page
│   ├── page.tsx          # Server component
│   └── actions.ts        # Server actions
├── feedback/[cid]/       # Feedback form page
│   ├── page.tsx          # Server component
│   └── actions.ts        # Server actions
├── review/[cid]/         # Review link redirect
│   ├── page.tsx          # Server component
│   └── actions.ts        # Server actions
├── layout.tsx            # Root layout
├── page.tsx              # Home page
└── globals.css           # Global styles

components/
├── PortalForm.tsx        # WiFi portal form (client)
└── FeedbackForm.tsx      # Feedback form (client)
```

## Key Features

### WiFi Portal (`/portal/[rid]`)
- Mobile-optimized form
- Collects name, phone, terms acceptance
- Server-side restaurant data fetching
- Success confirmation screen

### Review Click Tracking (`/review/[cid]`)
- Logs click event server-side
- Immediately redirects to Google Review
- No UI shown to user (seamless redirect)

### Feedback Form (`/feedback/[cid]`)
- 5-star rating system
- Multi-select improvement areas
- Optional comment field
- Mobile-friendly interface

## Server Actions

All backend communication happens server-side via Next.js Server Actions:
- `submitCheckin()` - Save customer WiFi checkin
- `getRestaurant()` - Fetch restaurant details
- `trackReviewClick()` - Log review link click
- `submitFeedback()` - Save customer feedback
- `getCustomerInfo()` - Fetch customer details

This keeps the FastAPI URL completely hidden from the browser.

## Deployment

### Vercel (Recommended)

1. Connect your Git repository to Vercel
2. Set environment variable: `FASTAPI_URL` to your backend URL
3. Deploy

```bash
# Or use Vercel CLI
npm i -g vercel
vercel
```

### Environment Variables in Production

- `FASTAPI_URL` - Your Railway/Render backend URL (e.g., https://your-app.railway.app)

## Mobile Optimization

All pages are designed mobile-first with:
- Responsive layouts
- Large touch targets
- Clear typography
- Optimized forms
- Fast load times

## Notes

- Never expose the FastAPI URL to the client
- All API calls go through Server Actions
- Forms include proper validation and error handling
- Success states guide users through the flow
