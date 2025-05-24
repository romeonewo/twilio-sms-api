from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AlertRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    alert_type: str = Field(..., regex="^(emergency|warning|info|weather|health|security)$")
    language: Optional[str] = Field("en", regex="^(en|ewe|twi)$")
    priority: Optional[str] = Field("medium", regex="^(low|medium|high|critical)$")
    is_active: Optional[bool] = True

class AlertResponse(BaseModel):
    id: int
    title: str
    message: str
    alert_type: str
    language: str
    priority: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    image_filename: Optional[str]
    
    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    alert_type: Optional[str] = Field(None, regex="^(emergency|warning|info|weather|health|security)$")
    language: Optional[str] = Field(None, regex="^(en|ewe|twi)$")
    priority: Optional[str] = Field(None, regex="^(low|medium|high|critical)$")
    is_active: Optional[bool] = None