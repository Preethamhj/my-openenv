# Reward model
from pydantic import BaseModel

class Reward(BaseModel):
    score: float