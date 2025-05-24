from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, LargeBinary
from sqlalchemy.sql import func
from database import Base

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), nullable=False)  # emergency, warning, info, etc.
    language = Column(String(10), default="en")  # en, ewe, twi
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # For imagery results as mentioned in requirements
    image_data = Column(LargeBinary, nullable=True)
    image_filename = Column(String(255), nullable=True)
    image_content_type = Column(String(100), nullable=True)

class AlertLog(Base):
    __tablename__ = "alert_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, nullable=False)
    recipient = Column(String(20), nullable=False)  # phone number
    status = Column(String(20), nullable=False)  # sent, failed, delivered
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)