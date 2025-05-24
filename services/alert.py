from sqlalchemy.orm import Session
from models import Alert, AlertLog
from schemas.alert import AlertRequest, AlertUpdate
from typing import List, Optional

def create_alert(db: Session, alert: AlertRequest) -> Alert:
    db_alert = Alert(
        title=alert.title,
        message=alert.message,
        alert_type=alert.alert_type,
        language=alert.language,
        priority=alert.priority,
        is_active=alert.is_active
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alerts(db: Session, skip: int = 0, limit: int = 100) -> List[Alert]:
    return db.query(Alert).offset(skip).limit(limit).all()

def get_alert_by_id(db: Session, alert_id: int) -> Optional[Alert]:
    return db.query(Alert).filter(Alert.id == alert_id).first()

def get_active_alerts(db: Session) -> List[Alert]:
    return db.query(Alert).filter(Alert.is_active == True).all()

def update_alert(db: Session, alert_id: int, alert_update: AlertUpdate) -> Optional[Alert]:
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if db_alert:
        update_data = alert_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_alert, field, value)
        db.commit()
        db.refresh(db_alert)
    return db_alert

def delete_alert(db: Session, alert_id: int) -> bool:
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if db_alert:
        db.delete(db_alert)
        db.commit()
        return True
    return False

def log_alert_notification(db: Session, alert_id: int, recipient: str, status: str, error_message: str = None):
    log_entry = AlertLog(
        alert_id=alert_id,
        recipient=recipient,
        status=status,
        error_message=error_message
    )
    db.add(log_entry)
    db.commit()
    return log_entry

def get_alert_logs(db: Session, alert_id: int) -> List[AlertLog]:
    return db.query(AlertLog).filter(AlertLog.alert_id == alert_id).all()