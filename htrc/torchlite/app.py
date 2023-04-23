from fastapi import FastAPI
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from htrc.ef.api import Api
from htrc.torchlite import Torchlite, Response, Status, __version__
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.widgets import TimeLineWidget, Widget
from htrc.torchlite.worksets import Workset as tl_Workset
from htrc.torchlite.filters import torchlite_stopword_filter, torchlite_stemmer, torchlite_lemmatizer
from htrc.torchlite.middleware import TorchliteVersionHeaderMiddleware


def setup_demo(app: Torchlite, ef_api: Api) -> None:
    app.add_workset(id="64407dbd3300005208a5dca4", description="DocSouth", volumes=82)

    app.add_workset(id="644070973300002108a5dca2", description="Freud Standard Edition", volumes=160)

    app.add_workset(id="644076b83300003608a5dca3", description="Seven Dada Manifests", volumes=10)

    app.add_workset(id="6418977d2d000079045c8287", description="New Jersey", volumes=419)

    demo_workset = tl_Workset("64407dbd3300005208a5dca4", ef_api)
    demo_dashboard = Dashboard()
    demo_dashboard.workset = demo_workset
    demo_dashboard.id = "demo"
    widget = TimeLineWidget()
    widget.id = "demo_widget"
    demo_dashboard.add_widget(widget)

    app.add_dashboard(demo_dashboard)
    app.register_filter("stopwords", torchlite_stopword_filter)
    app.register_filter("stemmer", torchlite_stemmer)
    app.register_filter("lemmatizer", torchlite_lemmatizer)


origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]

print(f"Starting Torchlite Backend v{__version__}")

api: fastapi.FastAPI = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.add_middleware(
    TorchliteVersionHeaderMiddleware,
)

ef_api: Api = Api()
app: Torchlite = Torchlite(ef_api)
setup_demo(app, ef_api)


@api.get("/")
async def read_root() -> Response:
    info: dict = app.info()
    if info:
        return Response(status=Status.success, data=list(info))
    else:
        return Response(status=Status.error, messages=list("could not get app info"))


@api.get("/worksets")
async def get_worksets() -> Response:
    worksets: list = app.worksets
    if worksets:
        return Response(status=Status.success, data=worksets)
    else:
        return Response(status=Status.error, messages=list("could not get worksets"))


@api.get("/worksets/{workset_id}")
async def get_workset(workset_id: str) -> Response:
    metadata = app.ef_api.get_workset_metadata(workset_id, ["metadata.title"])
    titles: list = []
    if metadata:
        titles = [v.metadata.title for v in metadata]
    return Response(status=Status.success, data=list({"id": workset_id, "metadata": titles}))


@api.get("/dashboards")
async def get_dashboards() -> Response:
    dashboards: dict = app.dashboards
    info_list: list = []
    if dashboards:
        info_list = [d.info for d in dashboards.values()]
    return Response(status=Status.success, data=info_list)


@api.post("/dashboards")
async def create_dashboard() -> Response:
    d = app.add_dashboard(Dashboard())
    return Response(status=Status.success, data=list(d.id))


@api.get("/dashboards/{dashboard_id}")
async def get_dashboard(dashboard_id: str) -> Response:
    db: Dashboard = app.get_dashboard(dashboard_id)
    data = []
    if db:
        data.append(db.info)
        return Response(status=Status.success, data=data)
    else:
        return Response(status=Status.error, messages=[f"could not find dashboard {dashboard_id}"])


@api.put("/dashboards/{dashboard_id}/workset/{workset_id}")
async def put_dashboard_workset(dashboard_id: str, workset_id: str) -> Response:
    dashboard: Dashboard = app.get_dashboard(dashboard_id)
    if dashboard:
        dashboard.workset = tl_Workset(workset_id, ef_api)
        return Response(status=Status.success, data=list(dashboard.info))
    else:
        return Response(status=Status.error, messages=[f"could not find dashboard {dashboard_id}"])


@api.post("/dashboards/{dashboard_id}/widgets/{widget_type}")
async def post_dashboard_widget(dashboard_id: str, widget_type: str) -> Response:
    dashboard = app.get_dashboard(dashboard_id)
    if not dashboard:
        return Response(status=Status.error, messages=[f"could not find dashboard {dashboard_id}"])
    widget_class = app.widgets[widget_type]
    if not widget_class:
        return Response(status=Status.error, messages=[f"could not find widget type {widget_type}"])
    widget = widget_class()
    dashboard.add_widget(widget)
    return Response(status=Status.success, data=list({"widget_id": widget.id}))


@api.get("/dashboards/{dashboard_id}/widget/{widget_id}/data")
async def get_widget_data(dashboard_id: str, widget_id: str) -> Response:
    dashboard: Dashboard = app.get_dashboard(dashboard_id)
    if not dashboard:
        return Response(status=Status.error, messages=[f"could not find dashboard {dashboard_id}"])

    workset = dashboard.workset
    if not workset:
        return Response(status=Status.error, messages=["dashboard has no workset"])

    widget: Widget = dashboard.get_widget(widget_id)
    if not widget:
        return Response(status=Status.error, messages=[f"could not find widget {widget_id}"])

    return Response(status=Status.success, data=widget.get_data(workset))
