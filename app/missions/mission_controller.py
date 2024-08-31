from fastapi import APIRouter

router = APIRouter()

@router.post("/missions")
def create_mission():
    return {"message": "Mission created"}

@router.get("/missions/{mission_id}")
def get_mission(mission_id: str):
    return {"mission_id": mission_id}
