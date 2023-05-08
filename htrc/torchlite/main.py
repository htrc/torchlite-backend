from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/dashboards/", response_model=schemas.Dashboard)
def create_dashboard(dashboard: schemas.DashboardCreate, db: Session = Depends(get_db)):
    return crud.create_dashboard(db=db, dashboard=dashboard)


@app.get("/dashboards/", response_model=list[schemas.Dashboard])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dashboards = crud.get_dashboards(db, skip=skip, limit=limit)
    return dashboards


@app.get("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def read_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    db_dashboard = crud.get_dashboard(db, dashboard_id=dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard


@app.post("/dashboards/{dashboard_id}/widgets/", response_model=schemas.Widget)
def create_widget_for_dashboard(dashboard_id: int, widget: schemas.WidgetCreate, db: Session = Depends(get_db)):
    widget = crud.create_dashboard_widget(db=db, widget=widget, dashboard_id=dashboard_id)
    return widget


@app.get("/widgets/", response_model=list[schemas.Widget])
def read_widgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    widgets = crud.get_widgets(db=db, skip=skip, limit=limit)
    return widgets
