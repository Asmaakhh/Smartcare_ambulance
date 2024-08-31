from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Location(BaseModel):
    city: str
    address: str

class GPS(BaseModel):
    x: float
    y: float
    z: float

class Contact(BaseModel):
    name: str
    phone: str
    email: str

class Ambulance(BaseModel):
    id: Optional[str]
    registrationNumber: str
    type: str
    status: str
    location: Location
    drivers: List[str] = []
    lastMaintenance: Optional[datetime] = None
    nextMaintenance: Optional[datetime] = None
    serviceHistory: List[str] = []
    administrator: Contact
    gps: GPS
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    admin_id: str
