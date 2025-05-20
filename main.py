from fastapi import FastAPI, HTTPException
from schemas.sms import SMSRequest
from services.sms import send_sms

app = FastAPI(
    title="Twilio SMS API",
    description="A professional API for sending SMS using Twilio and FastAPI.",
    version="1.0.0"
)

@app.post("/send-sms", summary="Send an SMS message using Twilio")
def send_sms_endpoint(payload: SMSRequest):
    try:
        result = send_sms(payload.to, payload.message)
        return {"message": "SMS sent successfully", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
