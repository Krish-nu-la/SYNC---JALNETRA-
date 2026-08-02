from sqlalchemy.orm import Session

from app.models.report import Report


class ReportService:

    def create(self, db: Session, report):

        new_report = Report(**report.model_dump())

        db.add(new_report)

        db.commit()

        db.refresh(new_report)

        return new_report

    def get_all(self, db: Session):

        return db.query(Report).order_by(
            Report.created_at.desc()
        ).all()


report_service = ReportService()