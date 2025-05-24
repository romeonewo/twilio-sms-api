import requests
import json
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:8000"

# Mock user data for testing
MOCK_USERS = [
    {"phone": "+1234567890", "language": "en"},
    {"phone": "+1234567891", "language": "ewe"},
    {"phone": "+1234567892", "language": "twi"},
]

def test_create_alert():
    """Test creating a new alert"""
    alert_data = {
        "title": "Weather Warning",
        "message": "Heavy rainfall expected in the next 2 hours. Stay safe!",
        "alert_type": "weather",
        "language": "en",
        "priority": "high",
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/alerts", json=alert_data)
    print(f"Create Alert Response: {response.status_code}")
    if response.status_code == 200:
        alert = response.json()
        print(f"Created Alert ID: {alert['id']}")
        return alert['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_get_alerts():
    """Test retrieving all alerts"""
    response = requests.get(f"{BASE_URL}/alerts")
    print(f"Get Alerts Response: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total Alerts: {data['total']}")
        for alert in data['alerts']:
            print(f"- Alert {alert['id']}: {alert['title']} ({alert['priority']})")
    else:
        print(f"Error: {response.text}")

def test_send_sms():
    """Test sending SMS to mock users"""
    for user in MOCK_USERS:
        sms_data = {
            "to": user["phone"],
            "message": "This is a test message for alert system.",
            "language": user["language"],
            "alert_type": "info"
        }
        
        response = requests.post(f"{BASE_URL}/send-sms", json=sms_data)
        print(f"SMS to {user['phone']} ({user['language']}): {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")

def test_alert_notification(alert_id):
    """Test sending alert notifications to multiple users"""
    if not alert_id:
        print("No alert ID provided, skipping notification test")
        return
    
    recipients = [user["phone"] for user in MOCK_USERS]
    response = requests.post(f"{BASE_URL}/alerts/{alert_id}/notify", json=recipients)
    
    print(f"Alert Notification Response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Notifications sent: {result['notifications_sent']}")
        print(f"Notifications failed: {result['notifications_failed']}")
    else:
        print(f"Error: {response.text}")

def test_health_check():
    """Test API health check"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Health Check: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("🧪 Starting API Tests...")
    print("=" * 50)
    
    # Test health check
    print("\n1. Testing Health Check...")
    test_health_check()
    
    # Test creating alert
    print("\n2. Testing Create Alert...")
    alert_id = test_create_alert()
    
    # Test getting alerts
    print("\n3. Testing Get Alerts...")
    test_get_alerts()
    
    # Test SMS sending
    print("\n4. Testing SMS Sending...")
    test_send_sms()
    
    # Test alert notifications
    print("\n5. Testing Alert Notifications...")
    test_alert_notification(alert_id)
    
    print("\n" + "=" * 50)
    print("✅ Tests completed!")
    print("\nNote: SMS tests will only work with valid Twilio credentials and phone numbers.")