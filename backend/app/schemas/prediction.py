from pydantic import BaseModel


class NowcastRequest(BaseModel):
    rainfallMmHr: float
    timeOffsetMin: int


class ZonePrediction(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    depthCm: float
    risk: float
    level: str
    population: int
    trend: str


class NowcastResponse(BaseModel):
    generatedAt: str
    rainfallMmHr: float
    timeOffsetMin: int
    zones: list[ZonePrediction]