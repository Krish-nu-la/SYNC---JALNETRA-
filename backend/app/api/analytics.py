from fastapi import APIRouter

from app.services.analytics_service import analytics_service

router = APIRouter()


@router.get("/analytics")
def analytics(rain: float):

    return analytics_service.generate(rain)