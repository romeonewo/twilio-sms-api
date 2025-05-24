from pydantic import BaseModel, Field
from typing import Optional, List

class SMSRequest(BaseModel):
    to: str = Field(..., description="Recipient phone number")
    message: str = Field(..., min_length=1, description="Message content")
    language: Optional[str] = Field("en", pattern="^(en|ewe|twi)$", description="Language for the message")
    alert_type: Optional[str] = Field(None, description="Type of alert for formatting")

class BulkSMSRequest(BaseModel):
    recipients: List[str] = Field(..., description="List of recipient phone numbers")
    message: str = Field(..., min_length=1, description="Message content")
    language: Optional[str] = Field("en", pattern="^(en|ewe|twi)$", description="Language for the message")
    alert_type: Optional[str] = Field(None, description="Type of alert for formatting")
