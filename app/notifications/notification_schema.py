from pydantic import BaseModel

class NotificationCreateSchema(BaseModel):
    clinic_id: str
    message: str
    status: str  # e.g., 'sent', 'received'

class NotificationResponseSchema(BaseModel):
    id: str
    clinic_id: str
    message: str
    status: str

class NotificationUpdateSchema(BaseModel):
    clinic_id: Optional[str]
    message: Optional[str]
    status: Optional[str]
