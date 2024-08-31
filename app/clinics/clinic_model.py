from pydantic import BaseModel
from typing import List, Optional

class ClinicContactInfo(BaseModel):
    phone: str
    email: str

class Doctor(BaseModel):
    name: str
    specialty: str
    phone: str

class Clinic(BaseModel):
    id: str
    clinicId: str
    name: str
    capacity: int
    location: str
    services: List[str]
    contactInfo: ClinicContactInfo
    doctors: List[Doctor]
    ambulances: List[str]
    status: str
    admin_id: str
