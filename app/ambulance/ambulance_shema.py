from pydantic import BaseModel
from typing import Optional

class AmbulanceCreateSchema(BaseModel):
    license_plate: str
    status: str  # e.g., 'available', 'busy'
    driver_id: Optional[str]

class AmbulanceResponseSchema(BaseModel):
    id: str
    license_plate: str
    status: str
    driver_id: Optional[str]

class AmbulanceUpdateSchema(BaseModel):
    license_plate: Optional[str]
    status: Optional[str]
    driver_id: Optional[str]
