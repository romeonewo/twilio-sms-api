from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.sms import SMSRequest
from schemas.alert import AlertRequest, AlertResponse
from services.sms import send_sms
from services.alert import create_alert, get_alerts, get_alert_by_id
from database import get_db
import uvicorn

app = FastAPI(
    title="Twilio SMS & Alert API",
    description="Send SMS messages using Twilio + FastAPI with Alert management system.",
    version="1.0.0"
)

@app.post("/send-sms", summary="Send an SMS")
def send_sms_endpoint(payload: SMSRequest):
    try:
        result = send_sms(payload.to, payload.message, payload.language)
        return {"message": "SMS sent successfully", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/alerts", response_model=AlertResponse, summary="Create a new alert")
def create_alert_endpoint(alert: AlertRequest, db: Session = Depends(get_db)):
    try:
        db_alert = create_alert(db, alert)
        return db_alert
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts", summary="Get all alerts")
def get_alerts_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        alerts = get_alerts(db, skip=skip, limit=limit)
        return {"alerts": alerts, "total": len(alerts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts/{alert_id}", response_model=AlertResponse, summary="Get alert by ID")
def get_alert_endpoint(alert_id: int, db: Session = Depends(get_db)):
    try:
        alert = get_alert_by_id(db, alert_id)
        if alert is None:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/alerts/{alert_id}/notify", summary="Send alert notifications via SMS")
def notify_alert_endpoint(alert_id: int, recipients: list[str], db: Session = Depends(get_db)):
    try:
        alert = get_alert_by_id(db, alert_id)
        if alert is None:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        notifications_sent = []
        for recipient in recipients:
            try:
                result = send_sms(recipient, alert.message, alert.language or "en")
                notifications_sent.append({
                    "recipient": recipient,
                    "status": "sent",
                    "details": result
                })
            except Exception as sms_error:
                notifications_sent.append({
                    "recipient": recipient,
                    "status": "failed",
                    "error": str(sms_error)
                })
        
        return {
            "alert_id": alert_id,
            "notifications_sent": len([n for n in notifications_sent if n["status"] == "sent"]),
            "notifications_failed": len([n for n in notifications_sent if n["status"] == "failed"]),
            "details": notifications_sent
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", summary="Health check")
def root():
    return {"message": "Twilio SMS & Alert API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)