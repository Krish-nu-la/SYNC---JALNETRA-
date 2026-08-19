from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.report import Report


class ReportService:

    def create(self, db: Session, report):

        new_report = Report(
            **report.model_dump()
        )

        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        return new_report

    def get_all(self, db: Session):

        return (
            db.query(Report)
            .order_by(
                Report.created_at.desc()
            )
            .all()
        )

    def get_recent(
        self,
        db: Session,
        minutes: int = 60
    ):

        since = (
            datetime.utcnow()
            - timedelta(minutes=minutes)
        )

        return (
            db.query(Report)
            .filter(
                Report.created_at >= since
            )
            .order_by(
                Report.created_at.desc()
            )
            .all()
        )

    def get_zone_reports(
        self,
        db: Session,
        zone: str,
        minutes: int = 60
    ):

        since = (
            datetime.utcnow()
            - timedelta(minutes=minutes)
        )

        return (
            db.query(Report)
            .filter(
                Report.zone == zone,
                Report.created_at >= since
            )
            .order_by(
                Report.created_at.desc()
            )
            .all()
        )


report_service = ReportService()