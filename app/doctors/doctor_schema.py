from typing import Optional
from pydantic import BaseModel

class DoctorCreateSchema(BaseModel):
    name: str
    specialty: str
    clinic_id: Optional[str] = None

class DoctorResponseSchema(BaseModel):
    id: str
    name: str
    specialty: str
    clinic_id: Optional[str] = None

class DoctorUpdateSchema(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    clinic_id: Optional[str] = None


