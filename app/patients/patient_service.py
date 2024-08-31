from app.config import patient_collection, notification_collection
from bson import ObjectId
from fastapi import HTTPException
from patients import patient_model

async def select_healthcare_facility_service(patient_id: str, facility_type: str):
    # Validate facility_type (e.g., "clinic", "hospital", "doctor")
    if facility_type not in ["clinic", "hospital", "doctor"]:
        raise HTTPException(status_code=400, detail="Invalid facility type")

    # Update patient record with selected facility
    update_result = await patient_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": {"selectedFacility": facility_type}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found or no changes made")

    # Create a notification for the drivers
    notification = {
        "message": f"Patient {patient_id} selected a {facility_type}.",
        "type": "facility_selection",
        "patient_id": patient_id,
        "facility_type": facility_type
    }
    await notification_collection.insert_one(notification)

    
async def find_patient_by_id(patient_id: str):
    return await patient_model.find_one({"_id": patient_id})

async def update_patient_facility(patient_id: str, facility_type: str):
    # Update the facilityType in the patient document
    result = await patient_model.update_one(
        {"_id": patient_id},
        {"$set": {"facilityType": facility_type}}
    )
    return result