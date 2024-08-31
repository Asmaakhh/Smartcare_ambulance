from pydantic import BaseModel
from typing import List, Optional

class EmergencyContact(BaseModel):
    name: str
    phone: str

class Patient(BaseModel):
    id: str
    patientId: int
    name: str
    age: int
    address: str
    medicalHistory: List[str]
    emergencyContact: EmergencyContact
    admin_id: str
