from fastapi import APIRouter

from app.services.forecast_service import forecast_service

router = APIRouter()


@router.get("/forecast")
def forecast(rain: float):

    return forecast_service.generate(rain)