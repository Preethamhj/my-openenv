# Action model
from pydantic import BaseModel

class Action(BaseModel):
    action: str