from datetime import datetime

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):

    zone: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    description: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    severity: str = Field(
        ...,
        pattern="^(low|medium|high|severe)$"
    )

    latitude: float = Field(
        ...,
        ge=8.0,
        le=13.0
    )

    longitude: float = Field(
        ...,
        ge=74.0,
        le=78.0
    )

    depth_cm: float | None = Field(
        default=None,
        ge=0,
        le=200
    )

    road_blocked: bool = False


class ReportResponse(ReportCreate):

    id: int

    created_at: datetime

    class Config:
        from_attributes = True