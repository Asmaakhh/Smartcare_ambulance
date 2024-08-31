import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from app.main import app
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_select_healthcare_facility(mongo_mock):
    patient_collection = mongo_mock['patient_collection']
    notification_collection = mongo_mock['notification_collection']

    patient_id = "669a2ff9b68ce474d8cc898d"
    facility_type = "clinic"

    # Setup mock responses
    patient_collection.find_one.return_value = {
        "_id": patient_id,
        "name": "John Doe",
        "age": 30,
        "address": "456 Elm St",
        "medicalHistory": ["Hypertension", "Diabetes"],
        "emergencyContact": {"name": "Jane Doe", "phone": "123-456-7890"},
        "facilityType": "hospital"  # Original value
    }
    patient_collection.update_one.return_value = AsyncMock(modified_count=1)
    notification_collection.insert_one.return_value = None

    # Perform the request
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/api/patients/{patient_id}/select-facility",
            json={"facilityType": facility_type}  # Use the updated key
        )

    # Print out the response details for debugging
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    # Assert the response
    assert response.status_code == 200
    assert response.json() == {"message": "Facility selected and notification sent to drivers"}
