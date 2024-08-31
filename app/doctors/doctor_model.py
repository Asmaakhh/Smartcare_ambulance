from pydantic import BaseModel
from typing import Optional
import requests
from typing import Optional, List
from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException

client = MongoClient("mongodb://localhost:27017/")
db = client["Smart_Care"]

class Availability(BaseModel):
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str

class Doctor(BaseModel):
    id: str
    doctorId: int
    name: str
    clinicId: int
    specialty: str
    phone: str
    email: str
    yearsOfExperience: int
    availability: Availability
    admin_id: str

class DoctorResponseSchema(BaseModel):
    id: str
    name: str
    specialty: str
    clinic_id: Optional[str]

class DoctorUpdateSchema(BaseModel):
    name: Optional[str]
    specialty: Optional[str]
    clinic_id: Optional[str]


def get_doctor_by_id(doctor_id: str) -> DoctorResponseSchema:
    try:
        if not ObjectId.is_valid(doctor_id):
            raise HTTPException(status_code=400, detail="Invalid doctor ID format")
        
        doctor = db["doctors"].find_one({"_id": ObjectId(doctor_id)})
        if doctor:
            return DoctorResponseSchema(**doctor)
        else:
            raise HTTPException(status_code=404, detail="Doctor not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def assign_doctor_to_emergency_call(call_id: str, doctor_id: str) -> bool:
    # Logic to assign doctor to emergency call
    # Notify the doctor about the assignment
    return True

def get_patient_data(patient_id: str) -> Optional[dict]:
    # Logic to retrieve patient data from database
    pass

def get_ambulance_info(ambulance_id: str) -> Optional[dict]:
    # Logic to retrieve ambulance information
    pass

def get_assigned_personnel(call_id: str) -> Optional[dict]:
    # Logic to retrieve personnel assigned to the emergency call
    pass

def get_fastest_route(start_location: dict, end_location: dict) -> dict:
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_location['lat']},{start_location['lng']}&destination={end_location['lat']},{end_location['lng']}&key={api_key}"
    response = requests.get(url)
    return response.json()

def notify_doctor(doctor_id: str, message: str):
    # Logic to send a notification to the doctor
    pass

def share_patient_file(patient_id: str, doctor_ids: List[str]):
    # Logic to share patient file with other doctors
    pass