from fastapi import APIRouter

from app.services.alert_service import alert_service

router = APIRouter()


@router.get("/alerts")
def alerts(rain: float):

    return alert_service.generate(rain)