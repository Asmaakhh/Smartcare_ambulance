import os
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/smart_car")

settings = Settings()

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client['smart_car']

# Définition des collections
admin_collection = db['regulators']
ambulance_collection = db['ambulances']
call_collection = db['calls']
clinic_collection = db['clinics']
doctor_collection = db['doctors']
drivers_collection = db['drivers']
mission_collection = db['missions']
notification_collection = db['notifications']
paramedic_collection = db['paramedics']
patient_collection = db['patients']
statistic_collection = db['statistics']
