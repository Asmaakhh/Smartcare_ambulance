from fastapi import APIRouter, HTTPException
from app.config import notification_collection
from bson import ObjectId
router = APIRouter()

@router.post("/notifications")
async def create_notification(notification: dict):
    result = await notification_collection.insert_one(notification)
    return {"message": "Notification created", "notification_id": str(result.inserted_id)}

@router.get("/notifications/{notification_id}")
async def get_notification(notification_id: str):
    notification = await notification_collection.find_one({"_id": ObjectId(notification_id)})
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification
