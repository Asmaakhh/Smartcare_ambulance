import sys 
import os 
# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import APIRouter
from calls.calls_schema import CallResponseSchema
from typing import List
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from config import call_collection, drivers_collection, notification_collection

router = APIRouter()

@router.post("/drivers")
def create_driver():
    return {"message": "Driver created"}

@router.get("/drivers/{driver_id}")
def get_driver(driver_id: str):
    return {"driver_id": driver_id}

@router.put("/drivers/{driver_id}")
def update_driver(driver_id: str):
    return {"message": "Driver updated"}

@router.delete("/drivers/{driver_id}")
def delete_driver(driver_id: str):
    return {"message": "Driver deleted"}

@router.put("/assign-driver/{call_id}/{driver_id}")
async def assign_driver(call_id: str, driver_id: str):
    # Update the call to assign the driver
    result = await call_collection.update_one(
        {"_id": ObjectId(call_id)},
        {"$set": {"driverId": driver_id, "status": "driver_assigned"}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Call not found")
    
    # Optionally, you can verify if the driver exists
    driver = await drivers_collection.find_one({"_id": ObjectId(driver_id)})
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    return {"status": "driver_assigned"}

@router.get("/drivers/{driver_id}/calls")
async def get_driver_calls(driver_id: str):
    calls = await call_collection.find({"driverId": driver_id}).to_list(length=100)
    if not calls:
        raise HTTPException(status_code=404, detail="No calls found for driver")
    return calls

@router.get("/drivers/{driver_id}/notifications")
async def get_driver_notifications(driver_id: str):
    notifications = await notification_collection.find({"driverId": driver_id}).to_list(length=100)
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for driver")
    return notifications