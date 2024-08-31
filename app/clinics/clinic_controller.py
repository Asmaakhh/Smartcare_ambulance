from fastapi import APIRouter, HTTPException
from app.config import clinic_collection

router = APIRouter()

@router.get("/clinics")
async def get_clinics():
    try:
        clinics = await clinic_collection.find().to_list(None)
        return {"clinics": clinics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching clinics: {e}")
