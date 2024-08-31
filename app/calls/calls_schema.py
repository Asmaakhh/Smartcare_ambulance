# app/models/call_schema.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CallDetails(BaseModel):
    name: str
    age: int
    condition: str
    location: str
    receiver: str

class CallCreateSchema(BaseModel):
    patient_id: str
    ambulance_id: Optional[str]
    status: str  # e.g., 'pending', 'in_progress', 'completed'
    details: Optional[str]
    timestamp: datetime
    callerType: str  # e.g., 'patient', 'clinic', etc.

class CallResponseSchema(BaseModel):
    id: str
    patient_id: str
    ambulance_id: Optional[str]
    driver_id: Optional[str]
    status: str
    details: Optional[str]
    timestamp: str
    callerType: str
    callDetails: Optional[dict]

class CallUpdateSchema(BaseModel):
    patient_id: Optional[str]
    ambulance_id: Optional[str]
    status: Optional[str]
    details: Optional[str]
    timestamp: Optional[datetime]
    callerType: Optional[str]
