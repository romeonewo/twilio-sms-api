from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to: str, message: str) -> dict:
    sms = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to
    )
    return {
        "sid": sms.sid,
        "status": sms.status,
        "to": sms.to
    }
