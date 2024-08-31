# app/models/patient_schema.py
from pydantic import BaseModel
from typing import Optional, List

class EmergencyContact(BaseModel):
    name: str
    phone: str

class PatientCreateSchema(BaseModel):
    name: str
    age: int
    address: str
    medicalHistory: List[str]
    emergencyContact: EmergencyContact
    facilityType: Optional[str]  # Added field

class PatientResponseSchema(BaseModel):
    id: str
    name: str
    age: int
    address: str
    medicalHistory: List[str]
    emergencyContact: EmergencyContact
    facilityType: Optional[str]  # Added field

class PatientUpdateSchema(BaseModel):
    name: Optional[str]
    age: Optional[int]
    address: Optional[str]
    medicalHistory: Optional[List[str]]
    emergencyContact: Optional[EmergencyContact]
    facilityType: Optional[str]  # Added field
