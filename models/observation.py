# Observation model
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HistoryEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    step: int | None = None
    stage: str | None = None
    action: str | None = None
    reward: float | None = Field(default=None, ge=0.0, le=1.0)


class ObservationData(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str | None = None
    difficulty_level: int | None = None
    step: int | None = None
    progress: float | None = Field(default=None, ge=0.0, le=1.0)
    stage_name: str | None = None
    instruction: str | None = None
    history: list[HistoryEntry | dict[str, Any]] = Field(default_factory=list)
    alert: str | None = None
    logs: list[str] = Field(default_factory=list)
    suspected_asset: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    incident: dict[str, Any] = Field(default_factory=dict)
    business_context: dict[str, Any] = Field(default_factory=dict)
    recovery_targets: list[str] = Field(default_factory=list)
    status: str | None = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("exclude_unset", True)
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)


class Observation(BaseModel):
    task: str
    data: ObservationData

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("exclude_unset", True)
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
