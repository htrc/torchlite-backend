from typing import List
from sqlalchemy.orm import Session, Query
from htrc.torchlite import models, schemas


def get_dashboard(db: Session, dashboard_id: int) -> models.Dashboard | None:
    result = db.query(models.Dashboard).filter(models.Dashboard.id == dashboard_id)
    if result:
        return result.first()
    else:
        return None


def get_dashboards(db: Session, skip: int = 0, limit: int = 100) -> List[models.Dashboard] | None:
    result = db.query(models.Dashboard).offset(skip).limit(limit)
    if result:
        return result.all()
    else:
        return None


def create_dashboard(db: Session, dashboard: schemas.DashboardCreate) -> models.Dashboard:
    db_dashboard = models.Dashboard()
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard


def create_dashboard_widget(
    db: Session, widget: schemas.WidgetCreate, dashboard_id: int, widget_type: str
) -> models.Widget:
    db_widget: models.Widget = models.Widget(**widget.dict(), widget_type=widget_type, dashboard_id=dashboard_id)
    db.add(db_widget)
    db.commit()
    db.refresh(db_widget)
    return db_widget


def set_dashboard_workset(db: Session, dashboard_id: int, workset_id: str) -> models.Dashboard | None:
    result: Query = db.query(models.Dashboard).filter(models.Dashboard.id == dashboard_id)
    if result:
        db_dashboard = result.first()
        if db_dashboard:
            db_dashboard.workset = workset_id
            db.commit()
            db.refresh(db_dashboard)
            return db_dashboard
        else:
            return None
    else:
        return None


def get_widget(db: Session, widget_id: int) -> models.Widget | None:
    result = db.query(models.Widget).filter(models.Widget.id == widget_id)
    if result:
        return result.first()
    else:
        return None


def get_widgets(db: Session, skip: int = 0, limit: int = 100) -> List[models.Widget] | None:
    result = db.query(models.Widget).offset(skip).limit(limit)
    if result:
        return result.all()
    else:
        return None
