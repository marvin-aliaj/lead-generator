"""
Test script for email functionality
Run this to test Resend email integration without running the full scheduler
"""

import os
from dotenv import load_dotenv
load_dotenv()

from email_service import (
    send_review_request_email,
    send_feedback_request_email,
    send_email
)

def test_basic_email():
    """Test basic email sending"""
    print("Testing basic email...")
    
    to_email = input("Enter recipient email: ")
    
    success = send_email(
        to_email=to_email,
        subject="Test Email from Restaurant System",
        html_content="<h1>Hello!</h1><p>This is a test email from your restaurant review system.</p>"
    )
    
    if success:
        print("✅ Basic email sent successfully!")
    else:
        print("❌ Failed to send basic email")
    
    return success


def test_review_request_email():
    """Test review request email"""
    print("\nTesting review request email...")
    
    to_email = input("Enter recipient email: ")
    customer_name = input("Enter customer name (default: John): ") or "John"
    restaurant_name = input("Enter restaurant name (default: Test Restaurant): ") or "Test Restaurant"
    review_link = "http://localhost:3000/review/test-customer-id"
    
    success = send_review_request_email(
        to_email=to_email,
        customer_name=customer_name,
        restaurant_name=restaurant_name,
        review_link=review_link
    )
    
    if success:
        print("✅ Review request email sent successfully!")
        print(f"   Check {to_email} for the email")
    else:
        print("❌ Failed to send review request email")
    
    return success


def test_feedback_request_email():
    """Test feedback request email"""
    print("\nTesting feedback request email...")
    
    to_email = input("Enter recipient email: ")
    customer_name = input("Enter customer name (default: John): ") or "John"
    restaurant_name = input("Enter restaurant name (default: Test Restaurant): ") or "Test Restaurant"
    feedback_link = "http://localhost:3000/feedback/test-customer-id"
    
    success = send_feedback_request_email(
        to_email=to_email,
        customer_name=customer_name,
        restaurant_name=restaurant_name,
        feedback_link=feedback_link
    )
    
    if success:
        print("✅ Feedback request email sent successfully!")
        print(f"   Check {to_email} for the email")
    else:
        print("❌ Failed to send feedback request email")
    
    return success


def main():
    print("=" * 80)
    print("Restaurant Review System - Email Testing")
    print("=" * 80)
    print()
    
    # Check environment variables
    from config import settings
    
    if not settings.resend_api_key or settings.resend_api_key == "your_resend_api_key":
        print("❌ RESEND_API_KEY not configured in .env file")
        print("   Please add your Resend API key to continue")
        return
    
    print(f"✅ Resend API key found")
    print(f"✅ From email: {settings.resend_from_email}")
    print()
    
    # Test menu
    while True:
        print("\nChoose a test:")
        print("1. Test basic email")
        print("2. Test review request email")
        print("3. Test feedback request email")
        print("4. Run all tests")
        print("0. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            test_basic_email()
        elif choice == "2":
            test_review_request_email()
        elif choice == "3":
            test_feedback_request_email()
        elif choice == "4":
            email = input("Enter recipient email for all tests: ")
            print("\n" + "=" * 80)
            print("Running all tests...")
            print("=" * 80)
            
            # Basic email
            send_email(
                to_email=email,
                subject="Test 1: Basic Email",
                html_content="<h1>Test 1</h1><p>Basic email test</p>"
            )
            
            # Review request
            send_review_request_email(
                to_email=email,
                customer_name="Test Customer",
                restaurant_name="Test Restaurant",
                review_link="http://localhost:3000/review/test-id"
            )
            
            # Feedback request
            send_feedback_request_email(
                to_email=email,
                customer_name="Test Customer",
                restaurant_name="Test Restaurant",
                feedback_link="http://localhost:3000/feedback/test-id"
            )
            
            print("\n✅ All tests completed!")
            print(f"   Check {email} inbox for 3 emails")
            
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice, please try again")


if __name__ == "__main__":
    main()
