import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import AsyncMock
from app.patients.patient_service import select_healthcare_facility_service
from bson import ObjectId
from app.patients import patient_model
@pytest.mark.asyncio
async def test_select_healthcare_facility_service(mongo_mock):
    # Mock collections
    patient_collection = mongo_mock['patient_collection']
    notification_collection = mongo_mock['notification_collection']
    
    # Mock patient and notification data
    patient_id = "608d1c5b2f1d8e3d2b8b4567"
    facility_type = "clinic"
    
    # Mock patient update result
    patient_collection.update_one = AsyncMock(return_value=AsyncMock(modified_count=1))
    
    # Mock notification insertion
    notification_collection.insert_one = AsyncMock()

    await select_healthcare_facility_service(patient_id, facility_type)
    
    # Verify that patient collection update was called with correct parameters
    patient_collection.update_one.assert_called_with(
        {"_id": ObjectId(patient_id)},
        {"$set": {"facility_type": facility_type}}
    )
    
    # Verify that notification was inserted with correct parameters
    notification_collection.insert_one.assert_called_with({
        "patient_id": patient_id,
        "facility_type": facility_type
    })

