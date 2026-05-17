-- Supabase Schema for Restaurant Review & Feedback Automation System

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Restaurants table
CREATE TABLE IF NOT EXISTS restaurants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    review_link TEXT NOT NULL
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    restaurant_id UUID NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    message_sent BOOLEAN DEFAULT FALSE,
    message_sent_at TIMESTAMPTZ,
    review_clicked BOOLEAN DEFAULT FALSE,
    review_clicked_at TIMESTAMPTZ,
    feedback_sent BOOLEAN DEFAULT FALSE
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    restaurant_id UUID NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    improvement_areas TEXT[] NOT NULL,
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_customers_created_at ON customers(created_at);
CREATE INDEX IF NOT EXISTS idx_customers_message_sent ON customers(message_sent);
CREATE INDEX IF NOT EXISTS idx_customers_review_clicked ON customers(review_clicked);
CREATE INDEX IF NOT EXISTS idx_customers_feedback_sent ON customers(feedback_sent);
CREATE INDEX IF NOT EXISTS idx_customers_message_sent_at ON customers(message_sent_at);
CREATE INDEX IF NOT EXISTS idx_feedback_customer_id ON feedback(customer_id);
CREATE INDEX IF NOT EXISTS idx_feedback_restaurant_id ON feedback(restaurant_id);

-- Insert a default restaurant for the pilot
INSERT INTO restaurants (name, review_link) 
VALUES ('Demo Restaurant', 'https://g.page/r/YOUR_GOOGLE_REVIEW_LINK/review')
ON CONFLICT DO NOTHING;
