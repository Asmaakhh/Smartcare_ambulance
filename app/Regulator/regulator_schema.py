# app/schemas/schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import List

class RegulatorSchema(BaseModel):
    id: str
    name: str
    clinicId: str  # Assuming the regulator has an associated clinic ID