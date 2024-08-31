from pydantic import BaseModel

class MissionCreateSchema(BaseModel):
    call_id: str
    driver_id: Optional[str]
    status: str  # e.g., 'pending', 'in_progress', 'completed'

class MissionResponseSchema(BaseModel):
    id: str
    call_id: str
    driver_id: Optional[str]
    status: str

class MissionUpdateSchema(BaseModel):
    call_id: Optional[str]
    driver_id: Optional[str]
    status: Optional[str]
