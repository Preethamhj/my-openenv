# Reward model
from pydantic import BaseModel, Field


class Reward(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
