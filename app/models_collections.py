from pymongo import MongoClient
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.Smart_Care

# Define MongoDB collections
calls_collection = db.calls
clinics_collection = db.clinics
regulators_collection = db.regulators  # Example for regulator collection

# Optionally define additional collections if needed
