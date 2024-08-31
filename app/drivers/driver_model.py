from pydantic import BaseModel
from typing import Optional

class Shift(BaseModel):
    start: str
    end: str

class Driver(BaseModel):
    id: str
    chauffeurId: int
    name: str
    licenseNumber: str
    phone: str
    email: str
    vehicleId: int
    shift: Shift
    admin_id: str
