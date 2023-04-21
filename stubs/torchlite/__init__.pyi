from _typeshed import Incomplete
from htrc.ef.api import Api as Api
from htrc.torchlite.dashboards import Dashboard as Dashboard

class Torchlite:
    ef_api: Incomplete
    widgets: Incomplete
    worksets: Incomplete
    filter_factory: Incomplete
    def __init__(self, ef_api: Api) -> None: ...
    def info(self): ...
    def add_workset(self, **kwargs) -> None: ...
    @property
    def dashboards(self): ...
    def add_dashboard(self, dashboard: Dashboard): ...
    def get_dashboard(self, dashboard_id): ...
    def delete_dashboard(self, dashboard_id) -> None: ...
    @property
    def filters(self): ...
    def register_filter(self, key, fn) -> None: ...
    def get_filter(self, key): ...
    def delete_filter(self, key) -> None: ...
