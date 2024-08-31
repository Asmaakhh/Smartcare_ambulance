from pydantic import BaseModel
from typing import Optional

class Paramedic(BaseModel):
    id: str
    name: str
    licenseNumber: str
    phone: str
    email: str
    yearsOfExperience: int
    admin_id: str

