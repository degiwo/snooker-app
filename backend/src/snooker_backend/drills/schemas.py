from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Category(StrEnum):
    BREAK_BUILDING = "break_building"
    LONG_POTTING = "long_potting"
    REST = "rest"
    SAFETY = "safety"


class DrillBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    setup: str | None = Field(default=None, max_length=2000)
    attempts: int = Field(ge=1)
    max_points_per_attempt: int | None = Field(default=None, ge=1)  # None = unlimited
    category: Category


class DrillCreate(DrillBase):
    """What the client sends to create a drill."""


class DrillUpdate(DrillBase):
    """What the client sends to update an existing drill."""

    is_active: bool


class DrillRead(DrillBase):
    """What the API returns to the client."""

    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
