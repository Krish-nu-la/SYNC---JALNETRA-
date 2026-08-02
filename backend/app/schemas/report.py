from pydantic import BaseModel


class ReportCreate(BaseModel):

    zone: str

    description: str

    severity: str

    latitude: float

    longitude: float


class ReportResponse(ReportCreate):

    id: int

    class Config:

        from_attributes = True