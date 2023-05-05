import os
from typing import Optional
from pathlib import Path

from fastapi_healthchecks.api.router import HealthcheckRouter, Probe
from yaml import safe_load
import requests
from fastapi import FastAPI
import fastapi
from htrc.ef.api import Api
from htrc.torchlite import Torchlite, Response, Status, __version__
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.widgets import Widget
from htrc.torchlite.worksets import Workset as tl_Workset
from htrc.torchlite.filters import torchlite_stopword_filter, torchlite_stemmer, torchlite_lemmatizer
from htrc.torchlite.middleware import TorchliteVersionHeaderMiddleware
from urllib.parse import urlparse, ParseResult


class TorchliteError(Exception):
    """Torchlite error of some kind"""

    pass


env = os.getenv("ENV", "dev")
print(f"Starting Torchlite Backend v{__version__} ({env})")

config_file_name: Optional[str] = os.getenv("TORCHLITE_CONFIG")
if not config_file_name:
    raise TorchliteError("TORCHLITE_CONFIG value is invalid or not set")

print(f"Loading configuration from {config_file_name}...")
parse_result: ParseResult = urlparse(config_file_name)

if parse_result.scheme.startswith("http"):
    resp: requests.Response = requests.get(config_file_name)
    if resp.status_code == 200:
        config = safe_load(resp.text)
    else:
        raise TorchliteError(f"Could not load config {config_file_name} - HTTP error {resp.status_code}")
else:
    p: Path = Path(parse_result.path)
    try:
        with open(p, mode="r", encoding="utf-8-sig") as f:
            config = safe_load(f)
    except IOError as e:
        raise TorchliteError(f"could not load config file {config_file_name}") from e


def set_defaults(app: Torchlite, ef_api: Api, config: dict) -> None:
    for data in config["featured_worksets"]:
        app.add_workset(**data)

    app.register_filter("stopwords", torchlite_stopword_filter)
    app.register_filter("stemmer", torchlite_stemmer)
    app.register_filter("lemmatizer", torchlite_lemmatizer)


api: fastapi.FastAPI = FastAPI()
api.add_middleware(
    TorchliteVersionHeaderMiddleware,
)
api.include_router(
    HealthcheckRouter(
        Probe(
            name="readiness",
            checks=[],  # TBD
        ),
        Probe(
            name="liveness",
            checks=[],
        ),
    ),
    prefix="/health",
)

ef_api: Api = Api()
app: Torchlite = Torchlite(ef_api)
set_defaults(app, ef_api, config)


@api.get("/")
async def read_root() -> Response:
    info: dict = app.info()
    if info:
        return Response(status=Status.success, data=[info])
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
async def get_workset_by_id(workset_id: str) -> Response:
    metadata = app.ef_api.get_workset_metadata(workset_id, ["htid,metadata.title"])
    titles: list = []
    if metadata:
        titles = [{"htid": v.htid, "title": v.metadata.title} for v in metadata]
        return Response(status=Status.success, data=titles)
    else:
        return Response(status=Status.error, messages=["got no titles"])


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
    return Response(status=Status.success, data=[d.id])


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
        return Response(status=Status.success, data=[dashboard.info])
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
    return Response(status=Status.success, data=[{"widget_id": widget.id}])


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
