from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Translation dictionaries for common alert messages
TRANSLATIONS = {
    "emergency": {
        "en": "EMERGENCY ALERT: {message}",
        "ewe": "ƉEƉE BIABO: {message}",
        "twi": "AMOA KƆKƆBƆ: {message}"
    },
    "warning": {
        "en": "WARNING: {message}",
        "ewe": "NYAGBƆSE: {message}",
        "twi": "KƆKƆBƆ: {message}"
    },
    "info": {
        "en": "INFO: {message}",
        "ewe": "NUFIAFI: {message}",
        "twi": "AMANNEƐBƆ: {message}"
    },
    "weather": {
        "en": "WEATHER ALERT: {message}",
        "ewe": "YAME ƉEƉE: {message}",
        "twi": "EWIEM KƆKƆBƆ: {message}"
    },
    "health": {
        "en": "HEALTH ALERT: {message}",
        "ewe": "LÃMESẼ ƉEƉE: {message}",
        "twi": "AKWAHOSAN KƆKƆBƆ: {message}"
    }
}

def format_message_by_language(message: str, language: str = "en", alert_type: str = None) -> str:
    """Format message based on language and alert type"""
    if alert_type and alert_type in TRANSLATIONS and language in TRANSLATIONS[alert_type]:
        return TRANSLATIONS[alert_type][language].format(message=message)
    return message

def send_sms(to: str, message: str, language: str = "en", alert_type: str = None) -> dict:
    formatted_message = format_message_by_language(message, language, alert_type)
    
    sms = client.messages.create(
        body=formatted_message,
        from_=TWILIO_PHONE_NUMBER,
        to=to
    )
    return {
        "sid": sms.sid,
        "status": sms.status,
        "to": sms.to,
        "language": language,
        "formatted_message": formatted_message
    }

def send_bulk_sms(recipients: list, message: str, language: str = "en", alert_type: str = None) -> list:
    """Send SMS to multiple recipients"""
    results = []
    formatted_message = format_message_by_language(message, language, alert_type)
    
    for recipient in recipients:
        try:
            sms = client.messages.create(
                body=formatted_message,
                from_=TWILIO_PHONE_NUMBER,
                to=recipient
            )
            results.append({
                "recipient": recipient,
                "status": "sent",
                "sid": sms.sid,
                "sms_status": sms.status
            })
        except Exception as e:
            results.append({
                "recipient": recipient,
                "status": "failed",
                "error": str(e)
            })
    
    return results