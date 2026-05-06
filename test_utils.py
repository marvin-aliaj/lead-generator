"""
Test utilities and manual testing scripts for development.
Run this file to test individual components without waiting for scheduled jobs.
"""

from datetime import datetime, timedelta
from database import supabase
from messaging import send_whatsapp_message, create_review_request_message, create_feedback_request_message
from config import settings
import sys


def test_database_connection():
    """Test Supabase connection"""
    print("Testing database connection...")
    try:
        result = supabase.table("restaurants").select("*").limit(1).execute()
        print("✅ Database connection successful")
        if result.data:
            print(f"   Found restaurant: {result.data[0]['name']}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False


def test_whatsapp_message(phone_number: str):
    """Test sending a WhatsApp message"""
    print(f"Testing WhatsApp message to {phone_number}...")
    try:
        message = "🧪 Test message from Restaurant Review System. If you receive this, everything is working!"
        success = send_whatsapp_message(phone_number, message)
        if success:
            print("✅ WhatsApp message sent successfully")
            return True
        else:
            print("❌ WhatsApp message failed to send")
            return False
    except Exception as e:
        print(f"❌ WhatsApp test failed: {str(e)}")
        return False


def create_test_customer(name: str = "Test Customer", phone: str = "+1234567890"):
    """Create a test customer in the database"""
    print(f"Creating test customer: {name}...")
    try:
        # Get first restaurant
        restaurant_result = supabase.table("restaurants").select("id").limit(1).execute()
        if not restaurant_result.data:
            print("❌ No restaurants found. Run schema.sql first!")
            return None
        
        restaurant_id = restaurant_result.data[0]["id"]
        
        # Create customer
        result = supabase.table("customers").insert({
            "name": name,
            "phone": phone,
            "restaurant_id": restaurant_id,
            "created_at": (datetime.now() - timedelta(hours=3)).isoformat()  # 3 hours ago for testing
        }).execute()
        
        if result.data:
            customer = result.data[0]
            print(f"✅ Test customer created with ID: {customer['id']}")
            return customer
        else:
            print("❌ Failed to create test customer")
            return None
    except Exception as e:
        print(f"❌ Error creating test customer: {str(e)}")
        return None


def test_review_request_flow(customer_id: str):
    """Test the review request message creation and sending"""
    print(f"Testing review request flow for customer {customer_id}...")
    try:
        # Get customer and restaurant data
        result = supabase.table("customers").select("*, restaurants(name, review_link)").eq("id", customer_id).execute()
        if not result.data:
            print("❌ Customer not found")
            return False
        
        customer = result.data[0]
        review_link = f"{settings.base_url}/review?cid={customer_id}"
        
        message = create_review_request_message(
            customer_name=customer["name"],
            restaurant_name=customer["restaurants"]["name"],
            review_link=review_link
        )
        
        print("\n📱 Message Preview:")
        print("-" * 50)
        print(message)
        print("-" * 50)
        
        # Ask if user wants to send
        send = input("\nSend this message? (y/n): ").strip().lower()
        if send == 'y':
            success = send_whatsapp_message(customer["phone"], message)
            if success:
                # Update database
                supabase.table("customers").update({
                    "message_sent": True,
                    "message_sent_at": datetime.now().isoformat()
                }).eq("id", customer_id).execute()
                print("✅ Review request sent and logged")
                return True
            else:
                print("❌ Failed to send message")
                return False
        else:
            print("Message not sent")
            return False
            
    except Exception as e:
        print(f"❌ Error in review request flow: {str(e)}")
        return False


def test_feedback_request_flow(customer_id: str):
    """Test the feedback request message creation and sending"""
    print(f"Testing feedback request flow for customer {customer_id}...")
    try:
        # Get customer and restaurant data
        result = supabase.table("customers").select("*, restaurants(name)").eq("id", customer_id).execute()
        if not result.data:
            print("❌ Customer not found")
            return False
        
        customer = result.data[0]
        feedback_link = f"{settings.base_url}/feedback?cid={customer_id}"
        
        message = create_feedback_request_message(
            customer_name=customer["name"],
            restaurant_name=customer["restaurants"]["name"],
            feedback_link=feedback_link
        )
        
        print("\n📱 Message Preview:")
        print("-" * 50)
        print(message)
        print("-" * 50)
        
        # Ask if user wants to send
        send = input("\nSend this message? (y/n): ").strip().lower()
        if send == 'y':
            success = send_whatsapp_message(customer["phone"], message)
            if success:
                # Update database
                supabase.table("customers").update({
                    "feedback_sent": True
                }).eq("id", customer_id).execute()
                print("✅ Feedback request sent and logged")
                return True
            else:
                print("❌ Failed to send message")
                return False
        else:
            print("Message not sent")
            return False
            
    except Exception as e:
        print(f"❌ Error in feedback request flow: {str(e)}")
        return False


def list_recent_customers(limit: int = 10):
    """List recent customers"""
    print(f"\nRecent customers (limit {limit}):")
    try:
        result = supabase.table("customers").select("*").order("created_at", desc=True).limit(limit).execute()
        if not result.data:
            print("No customers found")
            return
        
        for i, customer in enumerate(result.data, 1):
            print(f"\n{i}. {customer['name']} ({customer['phone']})")
            print(f"   ID: {customer['id']}")
            print(f"   Created: {customer['created_at']}")
            print(f"   Review sent: {customer['message_sent']}")
            print(f"   Review clicked: {customer['review_clicked']}")
            print(f"   Feedback sent: {customer['feedback_sent']}")
    except Exception as e:
        print(f"❌ Error listing customers: {str(e)}")


def interactive_menu():
    """Interactive testing menu"""
    while True:
        print("\n" + "=" * 50)
        print("Restaurant Review System - Testing Menu")
        print("=" * 50)
        print("1. Test database connection")
        print("2. Test WhatsApp messaging")
        print("3. Create test customer")
        print("4. List recent customers")
        print("5. Test review request flow")
        print("6. Test feedback request flow")
        print("7. Run all tests")
        print("0. Exit")
        print("=" * 50)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            test_database_connection()
        elif choice == "2":
            phone = input("Enter phone number (with country code, e.g., +1234567890): ").strip()
            test_whatsapp_message(phone)
        elif choice == "3":
            name = input("Enter customer name (default: Test Customer): ").strip() or "Test Customer"
            phone = input("Enter phone number (default: +1234567890): ").strip() or "+1234567890"
            create_test_customer(name, phone)
        elif choice == "4":
            list_recent_customers()
        elif choice == "5":
            customer_id = input("Enter customer ID: ").strip()
            test_review_request_flow(customer_id)
        elif choice == "6":
            customer_id = input("Enter customer ID: ").strip()
            test_feedback_request_flow(customer_id)
        elif choice == "7":
            print("\n🧪 Running all tests...\n")
            test_database_connection()
            print()
            phone = input("Enter your phone number to test WhatsApp (or press Enter to skip): ").strip()
            if phone:
                test_whatsapp_message(phone)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("🧪 Restaurant Review System - Test Utilities")
    print("=" * 50)
    
    # Check if running with arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "db":
            test_database_connection()
        elif command == "whatsapp" and len(sys.argv) > 2:
            test_whatsapp_message(sys.argv[2])
        elif command == "create":
            create_test_customer()
        elif command == "list":
            list_recent_customers()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python test_utils.py [db|whatsapp|create|list]")
    else:
        # Run interactive menu
        interactive_menu()
