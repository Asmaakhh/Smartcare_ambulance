import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import APIRouter, HTTPException, WebSocket
from typing import List
from doctors.doctor_model import (
    get_doctor_by_id,
    assign_doctor_to_emergency_call,
    get_patient_data,
    get_ambulance_info,
    get_assigned_personnel,
    get_fastest_route,
    notify_doctor,
    share_patient_file
)
from doctors.doctor_model import DoctorResponseSchema, DoctorUpdateSchema

router = APIRouter()

@router.get("/doctors/{doctor_id}", response_model=DoctorResponseSchema)
def read_doctor(doctor_id: str):
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/emergency-calls/{call_id}/assign/{doctor_id}")
def assign_doctor_to_emergency(call_id: str, doctor_id: str):
    result = assign_doctor_to_emergency_call(call_id, doctor_id)
    if not result:
        raise HTTPException(status_code=404, detail="Emergency call or doctor not found")
    return {"status": "Doctor assigned to emergency call"}

@router.get("/patients/{patient_id}")
def get_patient_info(patient_id: str):
    patient_data = get_patient_data(patient_id)
    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient data not found")
    return patient_data

@router.get("/ambulances/{ambulance_id}")
def get_ambulance_info(ambulance_id: str):
    info = get_ambulance_info(ambulance_id)
    if not info:
        raise HTTPException(status_code=404, detail="Ambulance information not found")
    return info

@router.get("/emergency-calls/{call_id}/personnel")
def get_assigned_personnel(call_id: str):
    personnel = get_assigned_personnel(call_id)
    if not personnel:
        raise HTTPException(status_code=404, detail="Personnel not found")
    return personnel

@router.get("/routes")
def get_route(start_location: dict, end_location: dict):
    route = get_fastest_route(start_location, end_location)
    return route

@router.post("/notifications/{doctor_id}")
def notify_doctor_of_assignment(doctor_id: str, message: str):
    notify_doctor(doctor_id, message)
    return {"status": "Notification sent"}

@router.post("/patients/{patient_id}/share")
def share_patient_record(patient_id: str, doctor_ids: List[str]):
    share_patient_file(patient_id, doctor_ids)
    return {"status": "Patient record shared"}
