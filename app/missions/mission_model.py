from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MissionTime(BaseModel):
    start: datetime
    end: Optional[datetime]

class Mission(BaseModel):
    id: str
    missionId: int
    callId: int
    patientId: int
    ambulanceId: int
    time: MissionTime
    notes: str
    location: str
    clinicId: int
    admin_id: str
