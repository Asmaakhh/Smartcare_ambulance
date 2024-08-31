import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import APIRouter, HTTPException
from typing import List
from Regulator.regulator_schema import RegulatorSchema
from calls.calls_schema import CallResponseSchema
from Regulator.regulator_service import fetch_clinic, fetch_urgent_calls_for_regulator, fetch_all_urgent_calls
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import logging
from Regulator.regulator_service import assign_driver

router = APIRouter()

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client.Smart_Care
regulators_collection = db.regulators

@router.get("/urgent-calls/{regulator_id}", response_model=List[CallResponseSchema])
async def get_urgent_calls(regulator_id: str):
    logging.debug(f"Fetching regulator with ID: {regulator_id}")
    regulator = await regulators_collection.find_one({"_id": ObjectId(regulator_id)})
    if not regulator:
        logging.error(f"Regulator with ID {regulator_id} not found")
        raise HTTPException(status_code=404, detail="Regulator not found")
    
    clinic_id = regulator.get("clinicId")
    if not clinic_id:
        logging.error(f"Regulator with ID {regulator_id} does not have an associated clinic")
        raise HTTPException(status_code=404, detail="Regulator does not have an associated clinic")
    
    urgent_calls = await fetch_urgent_calls_for_regulator(clinic_id)
    
    if not urgent_calls:
        logging.error(f"No urgent calls found for clinic ID {clinic_id}")
        raise HTTPException(status_code=404, detail="No urgent calls found for the regulator's clinic")
    
    for call in urgent_calls:
        call["id"] = str(call["_id"])
        del call["_id"]
    
    logging.debug(f"Returning urgent calls: {urgent_calls}")
    return urgent_calls

@router.get("/test-urgent-calls", response_model=List[CallResponseSchema])
async def test_urgent_calls():
    urgent_calls = await fetch_all_urgent_calls()
    
    if not urgent_calls:
        logging.error("No urgent calls found")
        raise HTTPException(status_code=404, detail="No urgent calls found")
    
    for call in urgent_calls:
        call["id"] = str(call["_id"])
        del call["_id"]
    
    logging.debug(f"Returning test urgent calls: {urgent_calls}")
    return urgent_calls

@router.put("/assign-driver/{call_id}/{driver_id}")
async def assign_driver_to_call(call_id: str, driver_id: str):
    # Assign the driver to the call
    result = await assign_driver(call_id, driver_id)
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Call not found or driver assignment failed")
    
    return {"message": f"Driver {driver_id} assigned to call {call_id}"}

