from fastapi import APIRouter

from app.services.dashboard_service import dashboard_service

router = APIRouter()


@router.get("/dashboard")
def dashboard(rain: float):

    return dashboard_service.build(rain)