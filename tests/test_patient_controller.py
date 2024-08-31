import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bson import ObjectId
patient_id = ObjectId("608d1c5b2f1d8e3d2b8b4567")
from fastapi import APIRouter, HTTPException
from app.main import app  # Import app from main.py
from app.config import patient_collection, notification_collection  # Import MongoDB collections

router = APIRouter()

@app.post("/api/patients/{patient_id}/select-facility")
async def select_healthcare_facility(patient_id: str, facility_type: str):
    patient = await patient_collection.find_one({"_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_result = await patient_collection.update_one(
        {"_id": patient_id},
        {"$set": {"facility_type": facility_type}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    await notification_collection.insert_one({"patient_id": patient_id, "facility_type": facility_type})

    return {"message": "Facility selected and notification sent to drivers"}
