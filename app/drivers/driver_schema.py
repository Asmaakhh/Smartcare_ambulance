from pydantic import BaseModel
from typing import Optional

class DriverCreateSchema(BaseModel):
    name: str
    license_number: str
    ambulance_id: Optional[str]

class DriverResponseSchema(BaseModel):
    id: str
    name: str
    license_number: str
    ambulance_id: Optional[str]

class DriverUpdateSchema(BaseModel):
    name: Optional[str]
    license_number: Optional[str]
    ambulance_id: Optional[str]
