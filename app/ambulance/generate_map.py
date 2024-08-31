import folium
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.Smart_Care
ambulances_collection = db.ambulances
clinics_collection = db.clinics

# Fetch ambulance locations
ambulances = ambulances_collection.find({})
# Fetch clinics
clinics = clinics_collection.find({})

# Create a map centered at an average location
map_center = [0, 0]
m = folium.Map(location=map_center, zoom_start=10)

# Add ambulance markers and calculate center
latitudes = []
longitudes = []

for ambulance in ambulances:
    gps = ambulance.get("gps", {})
    x, y = gps.get("x", 0), gps.get("y", 0)
    folium.Marker([y, x], popup=f"{ambulance.get('registrationNumber', 'Unknown')}<br>{ambulance.get('type', 'Unknown')}").add_to(m)
    latitudes.append(y)
    longitudes.append(x)

# Add clinic markers and paths
for clinic in clinics:
    gps = clinic.get("gps", {})
    x, y = gps.get("x", 0), gps.get("y", 0)
    # Add clinic marker
    folium.Marker([y, x], popup=f"Clinic: {clinic.get('name', 'Unknown')}", icon=folium.Icon(color='blue')).add_to(m)
    
    # Add paths from each ambulance to the clinic
    for ambulance in ambulances:
        amb_gps = ambulance.get("gps", {})
        amb_x, amb_y = amb_gps.get("x", 0), amb_gps.get("y", 0)
        folium.PolyLine(locations=[[amb_y, amb_x], [y, x]], color='green').add_to(m)

# Save the map to an HTML file
m.save("map.html")
