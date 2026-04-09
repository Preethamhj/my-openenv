# Action model
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: str = Field(..., min_length=1, description="Agent action text for the current stage.")

    @field_validator("action")
    @classmethod
    def validate_action_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("action must not be empty")
        return cleaned
