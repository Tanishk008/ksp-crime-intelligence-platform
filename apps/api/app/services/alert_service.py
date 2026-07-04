from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.schemas.alert import AlertCreate
from datetime import datetime
from typing import List, Optional

class AlertService:
    @staticmethod
    def get_alert(db: Session, alert_id: str) -> Optional[Alert]:
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @staticmethod
    def list_alerts(
        db: Session, 
        district_id: Optional[str] = None, 
        station_id: Optional[str] = None
    ) -> List[Alert]:
        query = db.query(Alert)
        if district_id:
            query = query.filter(Alert.district_id == district_id)
        if station_id:
            query = query.filter(Alert.station_id == station_id)
        return query.all()

    @staticmethod
    def acknowledge_alert(db: Session, alert_id: str, user_id: str) -> Optional[Alert]:
        alert = AlertService.get_alert(db, alert_id)
        if not alert:
            return None
        alert.acknowledged_by = user_id
        alert.acknowledged_at = datetime.utcnow()
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def create_alert(db: Session, alert_in: AlertCreate) -> Alert:
        db_alert = Alert(
            alert_type=alert_in.alert_type,
            severity=alert_in.severity,
            district_id=alert_in.district_id,
            station_id=alert_in.station_id,
            title=alert_in.title,
            description=alert_in.description,
            confidence_tier=alert_in.confidence_tier,
            supporting_data=alert_in.supporting_data
        )
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert
