import platform
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from htrc.torchlite.ef.workset import WorkSet
from backend import __version__
from backend.dashboard import Dashboard
from backend.torchlite import TorchLite
from backend.widgets import WidgetFactory
from backend.filters import *


app = TorchLite()

origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]


app.register_filter("stopwords", torchlite_stopword_filter)
app.register_filter("stemmer", torchlite_stemmer)
app.register_filter("lemmatizer", torchlite_lemmatizer)

app.add_workset(WorkSet('63f7ae452500006404fc54c7'))

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
    return {"sample_worksets": [w.htid for w in app.worksets.values()]}


@tlapi.get("/info")
def get_info():
    return {"version": __version__, "host": platform.node()}


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
    return {"dashboard": dashboard.id, "workset": workset.htid}


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
        result["workset"] = ws.htid
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
    return [ws.htid for ws in app.worksets.values()]


@tlapi.get("/worksets/{workset_id}")
def get_workset_by_id(workset_id):
    ws = app.get_workset(workset_id)
    return ws


#########
# Filters
#########


@tlapi.get("/filters")
def get_filters():
    return list(app.filters.keys())


@tlapi.get("/dashboards/{dashboard_id}/filters")
def get_dashboard_filters(dashboard_id: str):
    dashboard = app.get_dashboard(dashboard_id)
    return dashboard.token_filters


@tlapi.put("/dashboards/{dashboard_id}/filters")
def put_dashboard_filters(
    dashboard_id: str, filter: list[str] | None = Query(default=None)
):
    dashboard = app.get_dashboard(dashboard_id)
    dashboard.token_filters = filter
    return dashboard.token_filters


@tlapi.get("/dashboards/{dashboard_id}/tokens")
def get_dashboard_tokens(dashboard_id):
    '''
    The token list can be very large. During development,
    we cap the number of tokens returned at 100.
    '''
    dashboard = app.get_dashboard(dashboard_id)
    tokens = dashboard.tokens
    return tokens.most_common(100)
