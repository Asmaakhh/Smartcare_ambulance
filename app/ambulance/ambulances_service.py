import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient
from ambulance.ambulance_model import Ambulance
from bson import ObjectId
from typing import List, Dict

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.Smart_Care
ambulances_collection = db.ambulances

def get_ambulance_locations() -> List[Dict[str, float]]:
    # Retrieve only latitude and longitude fields
    ambulances = ambulances_collection.find({}, {"_id": 0, "latitude": 1, "longitude": 1})
    return list(ambulances)


def create_ambulance(ambulance: Ambulance) -> str:
    result = ambulances_collection.insert_one(ambulance.dict())
    return str(result.inserted_id)

def get_ambulance(ambulance_id: str) -> Ambulance:
    ambulance = ambulances_collection.find_one({"_id": ObjectId(ambulance_id)})
    return ambulance

def update_ambulance(ambulance_id: str, ambulance: Ambulance) -> bool:
    result = ambulances_collection.update_one({"_id": ObjectId(ambulance_id)}, {"$set": ambulance.dict()})
    return result.modified_count > 0

def delete_ambulance(ambulance_id: str) -> bool:
    result = ambulances_collection.delete_one({"_id": ObjectId(ambulance_id)})
    return result.deleted_count > 0
