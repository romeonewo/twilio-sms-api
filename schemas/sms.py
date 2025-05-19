from pydantic import BaseModel, Field

class SMSRequest(BaseModel):
    to: str = Field(..., example="+233532001476")
    message: str = Field(..., example="Hello from Twilio via FastAPI!")
