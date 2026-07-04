from sqlalchemy.orm import Session
from app.models.report import Report
from app.schemas.report import ReportCreate
from typing import List, Optional
import uuid

class ReportService:
    @staticmethod
    def get_report(db: Session, report_id: str) -> Optional[Report]:
        return db.query(Report).filter(Report.id == report_id).first()

    @staticmethod
    def list_reports(db: Session, user_id: str = None) -> List[Report]:
        query = db.query(Report)
        if user_id:
            query = query.filter(Report.created_by == user_id)
        return query.all()

    @staticmethod
    def create_report(db: Session, user_id: str, report_in: ReportCreate) -> Report:
        """
        Creates a new report draft.
        In production, this would queue a background task (e.g. Celery / Catalyst Event function)
        to compile the timeline and conversations into a PDF and upload it to Catalyst File Store.
        """
        db_report = Report(
            created_by=user_id,
            case_id=report_in.case_id,
            title=report_in.title,
            content_json={"status": "draft_created"},
            pdf_path=f"reports/{uuid.uuid4()}.pdf",
            status="DRAFT"
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report

    @staticmethod
    def delete_report(db: Session, report_id: str) -> bool:
        db_report = ReportService.get_report(db, report_id)
        if not db_report:
            return False
        db.delete(db_report)
        db.commit()
        return True
