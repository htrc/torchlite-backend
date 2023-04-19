from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from htrc.ef.api import Api
import htrc.ef.datamodels as ef
from htrc.torchlite import Torchlite
from htrc.torchlite.worksets import Workset as tl_Workset
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.widgets import TimeLineWidget
from htrc.torchlite.widgets.projectors import TimeLineProjector
from htrc.torchlite.filters import *

ef_api = Api()
app = Torchlite(ef_api)
origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.register_filter("stopwords", torchlite_stopword_filter)
app.register_filter("stemmer", torchlite_stemmer)
app.register_filter("lemmatizer", torchlite_lemmatizer)

startup_workset_ids = ['6418977d2d000079045c8287', '6416163a2d0000f9025c8284']

for id in startup_workset_ids:
    ws = tl_Workset(id, ef_api)
    app.add_workset(ws)


defaults = {}
defaults['workset'] = tl_Workset('6416163a2d0000f9025c8284', ef_api)


default_dashboard = Dashboard()
default_dashboard.workset = defaults["workset"]
default_dashboard.id = "default"
app.add_dashboard(default_dashboard)


@api.get("/")
async def read_root():
    app_info = app.info()
    return app_info | {"defaults": defaults}


@api.get("/worksets")
async def get_worksets():
    return app.worksets


@api.get("/worksets/{workset_id}")
async def get_workset(workset_id):
    obj = app.get_workset(workset_id)
    metadata = Api().get_volume_metadata(workset_id)
    return {'id': obj['workset'].id, 'metadata': metadata}


# @api.get("/dashboards")
# async def get_dashboards():
#     return [d.info for d in app.dashboards]


@api.get("/dashboards")
async def get_dashboards():
    return app.dashboards


@api.post("/dashboards")
def create_dashboard():
    d = Dashboard()
    app.add_dashboard(d)
    return app.get_dashboard(d.id)


@api.get("/dashboards/{dashboard_id}")
def get_dashboard(dashboard_id):
    if dashboard_id:
        return app.get_dashboard(dashboard_id)
    else:
        return None


@api.put("/dashboards/{dashboard_id}/workset/{workset_id}")
def put_dashboard_workset(dashboard_id: str, workset_id: str):
    dashboard = app.get_dashboard(dashboard_id)
    workset = app.get_workset(workset_id)  # fix to use torchlite workset
    dashboard.workset = workset
    return dashboard.info


@api.post("/dashboards/{dashboard_id}/widgets/{widget_type}")
def post_dashboard_widget(dashboard_id: str, widget_type: str):
    dashboard = app.get_dashboard(dashboard_id)
    widget_class = app.widgets[widget_type]
    widget = widget_class()
    dashboard.add_widget(widget)
    return dashboard


@api.get("/dashboards/{dashboard_id}/widget/{widget_id}/data")
async def get_widget_data(dashboard_id: str, widget_id: str):
    dashboard = app.get_dashboard(dashboard_id)
    widget = dashboard.get_widget(widget_id)
    return widget.get_data(dashboard.workset)
