from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.report import ReportCreate
from app.services.report_service import report_service


router = APIRouter()


@router.post("/reports")
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    return report_service.create(
        db,
        report
    )


@router.get("/reports")
def get_reports(
    db: Session = Depends(get_db)
):
    return report_service.get_all(db)


@router.get("/reports/recent")
def get_recent_reports(
    minutes: int = Query(
        default=60,
        ge=1,
        le=1440
    ),
    db: Session = Depends(get_db)
):
    return report_service.get_recent(
        db,
        minutes
    )


@router.get("/reports/zone/{zone}")
def get_zone_reports(
    zone: str,
    minutes: int = Query(
        default=60,
        ge=1,
        le=1440
    ),
    db: Session = Depends(get_db)
):
    return report_service.get_zone_reports(
        db,
        zone,
        minutes
    )