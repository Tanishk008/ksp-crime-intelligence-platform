from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.case import Case
import time

@celery_app.task(name="app.tasks.ingestion.ingest_cctns_case")
def ingest_cctns_case(case_data: dict):
    """
    Simulates async ingestion of CCTNS case records, performing validation and model mapping.
    """
    db = SessionLocal()
    try:
        print(f"Ingesting CCTNS record: {case_data.get('case_number')}...")
        time.sleep(1.0)
        
        existing = db.query(Case).filter(Case.case_number == case_data.get("case_number")).first()
        if existing:
             print("Case already exists.")
             return False
             
        new_case = Case(
            case_number=case_data.get("case_number"),
            case_type=case_data.get("case_type"),
            status=case_data.get("status", "ACTIVE"),
            station_id=case_data.get("station_id"),
            incident_address=case_data.get("incident_address"),
            narrative=case_data.get("narrative")
        )
        db.add(new_case)
        db.commit()
        print(f"Successfully ingested CCTNS case {case_data.get('case_number')}")
        return True
    except Exception as e:
        print(f"Failed ingesting CCTNS case: {e}")
        return False
    finally:
        db.close()
