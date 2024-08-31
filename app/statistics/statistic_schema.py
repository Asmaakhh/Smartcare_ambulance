from pydantic import BaseModel

class StatisticCreateSchema(BaseModel):
    metric: str
    value: float
    timestamp: str

class StatisticResponseSchema(BaseModel):
    id: str
    metric: str
    value: float
    timestamp: str

class StatisticUpdateSchema(BaseModel):
    metric: Optional[str]
    value: Optional[float]
    timestamp: Optional[str]
