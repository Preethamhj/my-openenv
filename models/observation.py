# Observation model
from pydantic import BaseModel

class Observation(BaseModel):
    task: str
    data: dict