from pydantic import BaseModel

class SMSRequest(BaseModel):
    to: str
    message: str

class AlertRequest(BaseModel):
    to: str
    alert_type: str  # e.g., "weather", "security", etc.
    content: str     # The actual message content
