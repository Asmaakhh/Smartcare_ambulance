from pydantic import BaseModel
from typing import Optional
class ClinicCreateSchema(BaseModel):
    name: str
    address: str
    contact_number: str

class ClinicResponseSchema(BaseModel):
    id: str
    name: str
    address: str
    contact_number: str

class ClinicUpdateSchema(BaseModel):
    name: Optional[str]
    address: Optional[str]
    contact_number: Optional[str]
