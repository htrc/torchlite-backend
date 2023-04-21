from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from htrc.ef.api import Api
from htrc.torchlite import Torchlite
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.filters import *
from htrc.torchlite.widgets import TimeLineWidget
from htrc.torchlite.worksets import Workset as tl_Workset


def setup_demo(app, ef_api):
    # startup_workset_ids = [
    #     '6418977d2d000079045c8287',
    #     '6416163a2d0000f9025c8284',
    #     '64407dbd3300005208a5dca4',
    # ]

    app.add_workset(id='64407dbd3300005208a5dca4', description='DocSouth', volumes=82)

    app.add_workset(
        id='644070973300002108a5dca2', description='Freud Standard Edition', volumes=160
    )

    app.add_workset(
        id='644076b83300003608a5dca3', description='Seven Dada Manifests', volumes=10
    )

    app.add_workset(
        id='6418977d2d000079045c8287', description="New Jersey", volumes=419
    )

    demo_workset = tl_Workset('64407dbd3300005208a5dca4', ef_api)
    demo_dashboard = Dashboard()
    demo_dashboard.workset = demo_workset
    demo_dashboard.id = 'demo'
    widget = TimeLineWidget()
    widget.id = 'TimeLineWidget'
    demo_dashboard.add_widget(widget)

    app.add_dashboard(demo_dashboard)
    app.register_filter("stopwords", torchlite_stopword_filter)
    app.register_filter("stemmer", torchlite_stemmer)
    app.register_filter("lemmatizer", torchlite_lemmatizer)


origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ef_api = Api()
app = Torchlite(ef_api)
setup_demo(app, ef_api)


@api.get("/")
async def read_root():
    app_info = app.info()
    return app_info


@api.get("/worksets")
async def get_worksets():
    return app.worksets


@api.get("/worksets/{workset_id}")
async def get_workset(workset_id):
    metadata = app.ef_api.get_workset_metadata(workset_id, ['metadata.title'])
    titles = [v.metadata.title for v in metadata]
    return {'id': workset_id, 'metadata': titles}


@api.get("/dashboards")
async def get_dashboards():
    return app.dashboards


@api.post("/dashboards")
async def create_dashboard():
    d = Dashboard()
    app.add_dashboard(d)
    return app.get_dashboard(d.id)


@api.get("/dashboards/{dashboard_id}")
async def get_dashboard(dashboard_id):
    if dashboard_id:
        return app.get_dashboard(dashboard_id)
    else:
        return None


@api.put("/dashboards/{dashboard_id}/workset/{workset_id}")
async def put_dashboard_workset(dashboard_id: str, workset_id: str):
    dashboard = app.get_dashboard(dashboard_id)
    dashboard.workset = tl_Workset(workset_id, ef_api)
    return dashboard.info


@api.post("/dashboards/{dashboard_id}/widgets/{widget_type}")
async def post_dashboard_widget(dashboard_id: str, widget_type: str):
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
