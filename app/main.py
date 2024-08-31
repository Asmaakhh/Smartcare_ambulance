import sys
import os
# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bson import ObjectId
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
import folium
import logging
from app.clinics.clinic_controller import router as clinic_router
from app.Regulator.regulator_controller import router as regulator_router
from doctors.doctor_controller import router as doctor_router
from drivers.driver_controller import router as drivers_router
from notifications.notification_controller import router as notification_router
from patients.patient_controller import router as patient_router

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
router = APIRouter()

# Include your routers here
app.include_router(clinic_router, prefix="/clinics")
app.include_router(regulator_router, prefix="/regulator", tags=["regulator"])
app.include_router(doctor_router, prefix="/api")
app.include_router(drivers_router, prefix="/api", tags=["drivers"])
app.include_router(patient_router, prefix="/api")
app.include_router(notification_router, prefix="/api", tags=["notifications"])

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.Smart_Care
ambulances_collection = db.ambulances
clinics_collection = db.clinics
drivers_collection = db.drivers
calls_collection = db.calls
regulators_collection = db.regulators
patient_collection = db.patient_collection
notification_collection = db.notification_collection

@app.get("/")
def read_root():
    return {"status": "ready"}

@app.get("/map", response_class=HTMLResponse)
async def get_map():
    # Fetch ambulance and clinic locations
    ambulances = list(ambulances_collection.find({}))
    clinics = list(clinics_collection.find({}))

    if not ambulances and not clinics:
        return HTMLResponse(content="<p>No data available.</p>")

    # Create a map centered at the average location of all ambulances and clinics
    all_latitudes = [ambulance.get("gps", {}).get("y", 0) for ambulance in ambulances] + \
                    [clinic.get("gps", {}).get("y", 0) for clinic in clinics]
    all_longitudes = [ambulance.get("gps", {}).get("x", 0) for ambulance in ambulances] + \
                     [clinic.get("gps", {}).get("x", 0) for clinic in clinics]

    if all_latitudes and all_longitudes:
        map_center = [sum(all_latitudes) / len(all_latitudes), sum(all_longitudes) / len(all_longitudes)]
    else:
        map_center = [0, 0]

    m = folium.Map(location=map_center, zoom_start=10)

    # Add ambulance markers
    for ambulance in ambulances:
        gps = ambulance.get("gps", {})
        x, y = gps.get("x", 0), gps.get("y", 0)
        folium.Marker([y, x], popup=f"{ambulance.get('registrationNumber', 'Unknown')}<br>{ambulance.get('type', 'Unknown')}").add_to(m)

    # Add clinic markers
    for clinic in clinics:
        gps = clinic.get("gps", {})
        x, y = gps.get("x", 0), gps.get("y", 0)
        folium.Marker([y, x], popup=f"{clinic.get('name', 'Unknown Clinic')}<br>{clinic.get('address', 'Unknown Address')}").add_to(m)

    # Draw paths between ambulances and clinics
    for ambulance in ambulances:
        ambulance_gps = ambulance.get("gps", {})
        amb_x, amb_y = ambulance_gps.get("x", 0), ambulance_gps.get("y", 0)
        for clinic in clinics:
            clinic_gps = clinic.get("gps", {})
            clin_x, clin_y = clinic_gps.get("x", 0), clinic_gps.get("y", 0)
            folium.PolyLine([(amb_y, amb_x), (clin_y, clin_x)], color="blue", weight=2.5, opacity=1).add_to(m)

    # Save the map to an HTML string
    html_content = m._repr_html_()
    return HTMLResponse(content=html_content)

@app.get("/test_map")
def test_map():
    map_center = [0, 0]
    m = folium.Map(location=map_center, zoom_start=2)
    folium.Marker([36, 10], popup="Test Marker").add_to(m)
    
    # Save to file for debugging
    with open("test_map.html", "w") as f:
        f.write(m._repr_html_())
    
    return HTMLResponse(content=m._repr_html_())

class FacilitySelection(BaseModel):
    facility_type: str

@app.post("/api/patients/{patient_id}/select-facility")
async def select_healthcare_facility(patient_id: str, facility_request: FacilitySelection):
    # Convert patient_id to ObjectId if necessary
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient ID")

    patient = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_result = await patient_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": {"facility_type": facility_request.facility_type}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    notification = {
        "message": f"Patient {patient_id} selected a {facility_request.facility_type}.",
        "type": "facility_selection",
        "patient_id": patient_id,
        "facility_type": facility_request.facility_type
    }
    await notification_collection.insert_one(notification)

    return {"message": "Facility selected and notification sent to drivers"}
