from fastapi import APIRouter

router = APIRouter()

@router.get("/statistics")
def get_statistics():
    return {"message": "Statistics"}
