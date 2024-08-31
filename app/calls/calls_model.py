from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CallDetails(BaseModel):
    name: str
    age: int
    condition: str
    location: str

class Call(BaseModel):
    id: str
    callId: int
    callerType: str
    timestamp: datetime
    details: CallDetails
    receiver: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    admin_id: str
