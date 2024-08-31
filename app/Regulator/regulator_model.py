
from pydantic import BaseModel

# Define the data models
class Regulator(BaseModel):
    id: str
    name: str
    clinicId: str

