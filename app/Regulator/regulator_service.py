import sys
import os
from typing import List
from bson import ObjectId
from models_collections import calls_collection, clinics_collection

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def fetch_clinic(clinic_id: str):
    try:
        return await clinics_collection.find_one({"_id": ObjectId(clinic_id)})
    except Exception as e:
        print(f"Error fetching clinic: {e}")
        return None

async def fetch_urgent_calls_for_regulator(regulator_clinic_id: str) -> List[dict]:
    try:
        # Ensure regulator_clinic_id is an ObjectId
        clinic_id = ObjectId(regulator_clinic_id)
        cursor = calls_collection.find({
            "clinicId": clinic_id,
            "priority": "urgent"
        })
        urgent_calls = []
        async for call in cursor:
            urgent_calls.append(call)
        return urgent_calls
    except Exception as e:
        print(f"Error fetching urgent calls: {e}")
        return []

async def fetch_all_urgent_calls() -> List[dict]:
    try:
        cursor = calls_collection.find({"priority": "urgent"})
        all_urgent_calls = []
        async for call in cursor:
            all_urgent_calls.append(call)
        return all_urgent_calls
    except Exception as e:
        print(f"Error fetching all urgent calls: {e}")
        return []

async def assign_driver(call_id: str, driver_id: str):
    try:
        result = await calls_collection.update_one(
            {"_id": ObjectId(call_id)},
            {"$set": {"driverId": driver_id, "status": "assigned"}}
        )
        if result.matched_count == 0:
            return {"message": "Call not found"}
        return {"message": "Driver assigned successfully"}
    except Exception as e:
        print(f"Error assigning driver: {e}")
        return {"message": "Error assigning driver"}
