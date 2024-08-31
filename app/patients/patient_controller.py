# app/controllers/patient_controller.py
from fastapi import APIRouter, HTTPException
from .patient_schema import PatientCreateSchema, PatientResponseSchema, PatientUpdateSchema
from app.config import patient_collection
from bson import ObjectId
from typing import List
from patients.patient_service import select_healthcare_facility_service, find_patient_by_id, update_patient_facility
router = APIRouter()

@router.post("/patients", response_model=PatientResponseSchema)
async def create_patient(patient: PatientCreateSchema):
    patient_data = patient.dict()
    result = await patient_collection.insert_one(patient_data)
    return {"id": str(result.inserted_id), **patient_data}

@router.get("/patients/{patient_id}", response_model=PatientResponseSchema)
async def get_patient(patient_id: str):
    patient = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "id": str(patient["_id"]),
        "name": patient["name"],
        "age": patient["age"],
        "address": patient["address"],
        "medicalHistory": patient.get("medicalHistory", []),
        "emergencyContact": patient.get("emergencyContact", {})
    }

@router.put("/patients/{patient_id}", response_model=PatientResponseSchema)
async def update_patient(patient_id: str, patient: PatientUpdateSchema):
    update_data = {k: v for k, v in patient.dict().items() if v is not None}
    result = await patient_collection.update_one({"_id": ObjectId(patient_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found or no changes made")
    updated_patient = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    return {
        "id": str(updated_patient["_id"]),
        "name": updated_patient["name"],
        "age": updated_patient["age"],
        "address": updated_patient["address"],
        "medicalHistory": updated_patient.get("medicalHistory", []),
        "emergencyContact": updated_patient.get("emergencyContact", {})
    }

@router.get("/patients", response_model=List[PatientResponseSchema])
async def list_patients():
    patients_cursor = patient_collection.find()
    patients = await patients_cursor.to_list(None)
    for patient in patients:
        patient["id"] = str(patient["_id"])
        del patient["_id"]  # Supprimer le champ _id pour éviter de le retourner
    return patients

@router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: str):
    result = await patient_collection.delete_one({"_id": ObjectId(patient_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted"}


@router.post("/patients/{patient_id}/select-facility")
async def select_healthcare_facility(patient_id: str, facility_type: str):
    try:
        await select_healthcare_facility_service(patient_id, facility_type)
        return {"message": "Facility selected and notification sent to drivers"}
    except HTTPException as e:
        raise e
    

@router.post("/api/patients/{patient_id}/select-facility")
async def select_facility(patient_id: str, facility_type: str):
    patient = await find_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found or no changes made")

    # Update patient with new facilityType
    await update_patient_facility(patient_id, facility_type)
    
    return {"message": "Facility selected and notification sent to drivers"}    