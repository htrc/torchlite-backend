import uuid
import json
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from htrc.torchlite.ef import WorkSet
from backend.dashboard import Dashboard
from backend.torchlite import TorchLite
from backend.widgets import WidgetFactory

app = TorchLite()

origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]


app.add_workset(
    WorkSet(
        url='https://worksets.htrc.illinois.edu/wsid/771d1500-7ac6-11eb-8593-e5f5ab8b1c01'
    )
)

mini_workset = WorkSet()
[
    mini_workset.add_volume(v_id)
    for v_id in ["uc1.32106011187561", "mdp.35112103187797", "uc1.$b684263"]
]
mini_workset.title = "minimal workset"
mini_workset.description = "minimal workset for testing"
app.add_workset(mini_workset)


app.add_dashboard(Dashboard("default"))


tlapi = FastAPI()

tlapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@tlapi.get("/")
def read_root():
    return {"sample_worksets": [w.description for w in app.worksets.values()]}


@tlapi.get("/dashboards")
def get_root_dashboard():
    return app.dashboards


@tlapi.get("/dashboards/{id}")
async def get_dashboard(id: str):
    try:
        d = app.get_dashboard(id)
        return {"dashboard": d.id, "widgets": [k for k in d.widgets.keys()]}

    except KeyError:
        raise HTTPException(status_code=404, detail="dashboard not found")


@tlapi.post("/dashboards")
def create_dashboard():
    d = Dashboard()
    app.add_dashboard(d)
    return {"dashboard": d.id}


def workset_metadata(workset):
    metadata = {}
    metadata['id'] = workset['id']


@tlapi.get("/dashboards/{dashboard_id}/workset")
def get_dashboard_workset(dashboard_id: str):
    result = {}
    dashboard = app.get_dashboard(dashboard_id)
    workset = dashboard.workset
    if workset:
        result = workset.metadata
    return result


@tlapi.put("/dashboards/{dashboard_id}/workset/{workset_id}")
def put_dashboard_workset(dashboard_id: str, workset_id: str):
    dashboard = app.get_dashboard(dashboard_id)
    workset = app.get_workset(workset_id)
    dashboard.workset = workset
    return {"dashboard": dashboard.id, "workset": workset.id}


@tlapi.get("/dashboards/{dashboard_id}/widgets")
def get_dashboard_widgets(dashboard_id: str):
    dashboard = app.get_dashboard(dashboard_id)
    return [k for k in dashboard.widgets.keys()]


@tlapi.post("/dashboards/{dashboard_id}/widgets/{widget_type}")
def post_dashboard_widget(dashboard_id: str, widget_type: str):
    dashboard = app.get_dashboard(dashboard_id)
    widget = WidgetFactory.make_widget(widget_type)
    dashboard.add_widget(widget)
    return {"widget": widget.id}


@tlapi.get("/dashboards/{dashboard_id}/widgets/{widget_id}")
def get_dashboard_widget(dashboard_id: str, widget_id: str):
    dashboard = app.get_dashboard(dashboard_id)
    widget = dashboard.get_widget(widget_id)
    result = {"id": widget.id}
    ws = widget.workset
    if widget.workset:
        result["workset"] = ws.id
    return result


@tlapi.get("/dashboards/{dashboard_id}/widgets/{widget_id}/data")
def get_widget_data(dashboard_id: str, widget_id: str):
    dashboard = app.get_dashboard(dashboard_id)
    widget = dashboard.get_widget(widget_id)
    return widget.data


##########
# Widgets
##########
@tlapi.get("/widgets")
def get_widgets():
    return app.widgets


##########
# WorkSets
##########
@tlapi.get("/worksets")
def get_worksets():
    return [ws.metadata for ws in app.worksets.values()]


@tlapi.get("/worksets/{workset_id}")
def get_workset_by_id(workset_id):
    ws = app.get_workset(workset_id)
    return ws
