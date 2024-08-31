from fastapi import APIRouter

router = APIRouter()

@router.post("/paramedics")
def create_paramedic():
    return {"message": "Paramedic created"}

@router.get("/paramedics/{paramedic_id}")
def get_paramedic(paramedic_id: str):
    return {"paramedic_id": paramedic_id}

@router.put("/paramedics/{paramedic_id}")
def update_paramedic(paramedic_id: str):
    return {"message": "Paramedic updated"}

@router.delete("/paramedics/{paramedic_id}")
def delete_paramedic(paramedic_id: str):
    return {"message": "Paramedic deleted"}
