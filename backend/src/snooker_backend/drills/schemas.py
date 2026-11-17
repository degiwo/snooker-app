from datetime import datetime

from pydantic import BaseModel, Field


class DrillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    setup: str | None = Field(default=None, max_length=2000)
    attempts: int = Field(ge=1)
    max_points_per_attempt: int | None = Field(default=None, ge=1)  # None = unlimited


class DrillRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str = Field(min_length=1, max_length=100)
    setup: str | None = Field(default=None, max_length=2000)
    attempts: int = Field(ge=1)
    max_points_per_attempt: int | None = Field(default=None, ge=1)  # None = unlimited
    is_active: bool = True
