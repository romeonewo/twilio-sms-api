from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sms import send_sms  # your sms.py Infobip function

app = FastAPI()

class SMSRequest(BaseModel):
    to: str
    text: str  # not "message" — to match Infobip

@app.post("/send-sms")
def send_sms_endpoint(sms: SMSRequest):
    try:
        response = send_sms(to=sms.to, text=sms.text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
