from fastapi import APIRouter

from .ambulance.ambulance_controller import router as ambulance_router
from .calls.calls_controller import router as call_router
from .clinics.clinic_controller import router as clinic_router
from .doctors.doctor_controller import router as doctor_router
from .drivers.driver_controller import router as driver_router
from .missions.mission_controller import router as mission_router
from .notifications.notification_controller import router as notification_router
from .paramedics.paramedic_controller import router as paramedic_router
from .patients.patient_controller import router as patient_router
from .statistics.statistic_controller import router as statistic_router
from .Regulator.regulator_controller import router as regulator_router  # Add this line

router = APIRouter(prefix="/api")

# Inclusion des routers spécifiques
router.include_router(ambulance_router)
router.include_router(call_router)
router.include_router(clinic_router)
router.include_router(doctor_router)
router.include_router(driver_router)
router.include_router(mission_router)
router.include_router(notification_router)
router.include_router(paramedic_router)
router.include_router(patient_router)
router.include_router(statistic_router)
router.include_router(regulator_router)  # Add this line
