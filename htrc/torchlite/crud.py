from sqlalchemy.orm import Session
from . import models, schemas


def get_dashboard(db: Session, dashboard_id: int):
    return db.query(models.Dashboard).filter(models.Dashboard.id == dashboard_id).first()


def get_dashboards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dashboard).offset(skip).limit(limit).all()


def create_dashboard(db: Session, dashboard: schemas.DashboardCreate):
    db_dashboard = models.Dashboard()
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def create_dashboard_widget(db: Session, widget: schemas.WidgetCreate, dashboard_id: int):
    db_widget = models.Widget(**widget.dict(), dashboard_id=dashboard_id)
    db.add(db_widget)
    db.commit()
    db.refresh(db_widget)
    return db_widget


def get_widgets(db: Session, skip: int = 0, limit: int = 100):
    widgets = db.query(models.Widget).offset(skip).limit(limit).all()
    return widgets
