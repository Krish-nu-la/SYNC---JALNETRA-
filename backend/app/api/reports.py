from fastapi import APIRouter, Depends
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

    return report_service.create(db, report)


@router.get("/reports")
def get_reports(

    db: Session = Depends(get_db)

):

    return report_service.get_all(db)