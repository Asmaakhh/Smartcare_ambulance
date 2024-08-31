from pydantic import BaseModel

class ParamedicCreateSchema(BaseModel):
    name: str
    certification_number: str

class ParamedicResponseSchema(BaseModel):
    id: str
    name: str
    certification_number: str

class ParamedicUpdateSchema(BaseModel):
    name: Optional[str]
    certification_number: Optional[str]
