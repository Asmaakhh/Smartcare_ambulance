# app/models/statistics_model.py
from pydantic import BaseModel
from typing import List, Optional

class CallFrequency(BaseModel):
    hourly: List[int]  # Liste des appels par heure
    daily: List[int]   # Liste des appels par jour

class AmbulanceUsage(BaseModel):
    totalDistance: float
    totalTime: float

class StatisticsBase(BaseModel):
    statId: int
    totalCalls: int
    acceptedCalls: int
    rejectedCalls: int
    callFrequency: CallFrequency
    ambulanceUsage: AmbulanceUsage
    updatedAt: Optional[str] = None

class StatisticsResponseSchema(StatisticsBase):
    id: str  # Utilisé pour la réponse en JSON
