
import sys 
import os 
# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# app/controllers/call_controller.py
from fastapi import APIRouter, HTTPException
from calls.calls_schema import CallCreateSchema, CallResponseSchema, CallUpdateSchema
from config import call_collection
from bson import ObjectId
from typing import List
from pydantic import BaseModel

router = APIRouter()

@router.post("/calls", response_model=CallResponseSchema)
async def create_call(call: CallCreateSchema):
    try:
        call_data = call.dict()
        result = await call_collection.insert_one(call_data)
        return {"id": str(result.inserted_id), **call_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating call: {str(e)}")

@router.put("/calls/{call_id}", response_model=CallResponseSchema)
async def update_call(call_id: str, call: CallUpdateSchema):
    try:
        update_data = {k: v for k, v in call.dict().items() if v is not None}
        result = await call_collection.update_one({"_id": ObjectId(call_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Call not found or no changes made")
        updated_call = await call_collection.find_one({"_id": ObjectId(call_id)})
        return {
            "id": str(updated_call["_id"]),
            "patient_id": updated_call["patient_id"],
            "ambulance_id": updated_call.get("ambulance_id"),
            "status": updated_call["status"],
            "details": updated_call.get("details"),
            "timestamp": updated_call["timestamp"],
            "callerType": updated_call["callerType"],
            "callDetails": updated_call.get("callDetails", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating call: {str(e)}")

@router.get("/calls", response_model=List[CallResponseSchema])
async def list_calls():
    try:
        calls_cursor = call_collection.find()
        calls = await calls_cursor.to_list(None)
        for call in calls:
            call["id"] = str(call["_id"])
            del call["_id"]  # Supprimer le champ _id pour éviter de le retourner
        return calls
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing calls: {str(e)}")

@router.put("/calls/{call_id}", response_model=CallResponseSchema)
async def update_call(call_id: str, call: CallUpdateSchema):
    try:
        update_data = {k: v for k, v in call.dict().items() if v is not None}
        result = await call_collection.update_one({"_id": ObjectId(call_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Call not found or no changes made")
        updated_call = await call_collection.find_one({"_id": ObjectId(call_id)})
        return {
            "id": str(updated_call["_id"]),
            "patient_id": updated_call["patient_id"],
            "ambulance_id": updated_call.get("ambulance_id"),
            "status": updated_call["status"],
            "details": updated_call.get("details"),
            "timestamp": updated_call["timestamp"],
            "callerType": updated_call["callerType"],
            "callDetails": updated_call.get("callDetails", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating call: {str(e)}")

@router.delete("/calls/{call_id}")
async def delete_call(call_id: str):
    try:
        result = await call_collection.delete_one({"_id": ObjectId(call_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Call not found")
        return {"message": "Call deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting call: {str(e)}")
