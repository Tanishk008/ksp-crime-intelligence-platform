from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.report import Report
import time

@celery_app.task(name="app.tasks.pdf_generation.compile_pdf_report")
def compile_pdf_report(report_id: str):
    """
    Background job task to generate PDF report from Case Timeline and Conversations.
    """
    db = SessionLocal()
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            print(f"Report {report_id} not found.")
            return False
            
        print(f"Compiling PDF for Report: {report.title}...")
        time.sleep(2.0)  # Simulate file IO compilation
        
        report.status = "GENERATED"
        report.content_json = {
            "summary": "This is a compiled cognitive investigation report detailing the timelines, resolved aliases, and competing hypotheses.",
            "pages_count": 3,
            "compiled_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        db.commit()
        print(f"Successfully compiled report {report_id}")
        return True
    except Exception as e:
        print(f"Failed compiling report: {e}")
        return False
    finally:
        db.close()
