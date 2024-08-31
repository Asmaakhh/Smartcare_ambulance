import asyncio
import pytest

@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

from unittest.mock import AsyncMock

@pytest.fixture
def mongo_mock(monkeypatch):
    # Mock patient_collection
    patient_mock = AsyncMock()
    # Mock notification_collection
    notification_mock = AsyncMock()

    # Patch the actual MongoDB collections
    monkeypatch.setattr('app.config.patient_collection', patient_mock)
    monkeypatch.setattr('app.config.notification_collection', notification_mock)

    # Return the mock objects
    return {
        'patient_collection': patient_mock,
        'notification_collection': notification_mock
    }
