import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi import APIRouter
from typing import List
from ambulance.ambulance_model import Ambulance
from ambulance.ambulances_service import get_ambulance_locations, create_ambulance, get_ambulance, update_ambulance, delete_ambulance

router = APIRouter()

@router.get("/ambulances/locations")
def get_ambulance_locations_route():
    locations = get_ambulance_locations()
    # Extract only the latitude and longitude from the Ambulance objects
    coordinates = [{"latitude": loc["latitude"], "longitude": loc["longitude"]} for loc in locations]
    return {"coordinates": coordinates}

@router.post("/ambulances")
def create_ambulance_route(ambulance: Ambulance):
    ambulance_id = create_ambulance(ambulance)
    return {"_id": ambulance_id}

@router.get("/ambulances/{ambulance_id}")
def get_ambulance_route(ambulance_id: str):
    ambulance = get_ambulance(ambulance_id)
    if ambulance:
        return ambulance
    else:
        return {"error": "Ambulance not found"}

@router.put("/ambulances/{ambulance_id}")
def update_ambulance_route(ambulance_id: str, ambulance: Ambulance):
    success = update_ambulance(ambulance_id, ambulance)
    if success:
        return {"message": "Ambulance updated"}
    else:
        return {"error": "Ambulance not found or no changes made"}

@router.delete("/ambulances/{ambulance_id}")
def delete_ambulance_route(ambulance_id: str):
    success = delete_ambulance(ambulance_id)
    if success:
        return {"message": "Ambulance deleted"}
    else:
        return {"error": "Ambulance not found"}

