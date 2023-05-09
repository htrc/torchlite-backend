from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from htrc.torchlite import crud, models, schemas, widgets
from htrc.torchlite.database import SessionLocal, engine
from htrc.torchlite.worksets import Workset
import htrc.ef.datamodels as ef
from htrc.ef.api import Api


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


widget_factory: widgets.WidgetFactory = widgets.WidgetFactory()

widget_factory.register_widget("timeline", widgets.TimeLineWidget)


@app.post("/dashboards/", response_model=schemas.Dashboard)
def create_dashboard(dashboard: schemas.DashboardCreate, db: Session = Depends(get_db)) -> models.Dashboard:
    return crud.create_dashboard(db=db, dashboard=dashboard)


@app.get("/dashboards/", response_model=list[schemas.Dashboard])
def read_dashboards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[models.Dashboard] | None:
    dashboards = crud.get_dashboards(db, skip=skip, limit=limit)
    return dashboards


@app.get("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def read_dashboard(dashboard_id: int, db: Session = Depends(get_db)) -> models.Dashboard | None:
    db_dashboard = crud.get_dashboard(db, dashboard_id=dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail=f"Dashboard {dashboard_id} not found")
    return db_dashboard


@app.post("/dashboards/{dashboard_id}/widgets/{widget_type}", response_model=schemas.Widget)
def create_widget_for_dashboard(
    dashboard_id: int, widget_type: str, widget: schemas.WidgetCreate, db: Session = Depends(get_db)
) -> models.Widget:
    widget = crud.create_dashboard_widget(db=db, widget=widget, dashboard_id=dashboard_id, widget_type=widget_type)
    return widget


@app.put("/dashboards/{dashboard_id}/workset/{workset_id}", response_model=schemas.Dashboard)
def update_dashboard_workset(
    dashboard_id: int, workset_id: str, db: Session = Depends(get_db)
) -> models.Dashboard | None:
    result = crud.set_dashboard_workset(db=db, dashboard_id=dashboard_id, workset_id=workset_id)
    return result


@app.get("/widgets/", response_model=list[schemas.Widget])
def read_widgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[models.Widget] | None:
    widgets = crud.get_widgets(db=db, skip=skip, limit=limit)
    return widgets


@app.get("/widgets/{widget_id}", response_model=schemas.Widget)
def read_widget(widget_id: int, db: Session = Depends(get_db)) -> models.Widget | None:
    db_widget = crud.get_widget(db, widget_id=widget_id)
    if db_widget is None:
        raise HTTPException(status_code=404, detail=f"Widget {widget_id} not found")
    return db_widget


@app.get("/widgets/{widget_id}/data")
def _get_widget_data(widget_id: int, db: Session = Depends(get_db)) -> Any:
    db_widget = crud.get_widget(db, widget_id=widget_id)
    if db_widget is None:
        raise HTTPException(status_code=404, detail=f"Widget {widget_id} not found")

    wsid = db_widget.dashboard.workset
    workset = Workset(wsid, Api())
    widget = widget_factory.make_widget(db_widget.widget_type)
    projection = widget.projection(workset)
    return projection


@app.get("/worksets/{workset_id}", response_model=ef.Workset)
def fetch_workset(workset_id: str, db: Session = Depends(get_db)) -> ef.Workset | None:
    ef_api = Api()
    workset: ef.Workset | None = ef_api.get_workset(workset_id)
    return workset
