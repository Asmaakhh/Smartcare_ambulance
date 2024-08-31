from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Notification(BaseModel):
    id: str
    notificationId: int
    sender: str
    receiver: str
    message: str
    timestamp: datetime
    read: bool
    admin_id: str
