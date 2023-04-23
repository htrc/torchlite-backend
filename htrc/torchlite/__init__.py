# -*- coding: utf-8 -*-
from typing import Callable, List, Union
from htrc.ef.api import Api
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.filters import FilterFactory
from htrc.torchlite.widgets import Widget

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("torchlite")
except PackageNotFoundError:
    __version__ = "UNKNOWN"


class Torchlite:
    def __init__(self, ef_api: Api) -> None:
        self.ef_api: Api = ef_api
        self._dashboards: dict = {}
        self.widgets: dict = {w.__name__: w for w in Widget.__subclasses__()}
        self.worksets: List = []
        self._filters: dict = {}
        self.filter_factory: FilterFactory = FilterFactory()

    def info(self) -> dict:
        return {"dashboards": self._dashboards, "widgets": self.widgets}

    def add_workset(self, **kwargs: Union[str, int]) -> None:
        self.worksets.append(kwargs)

    @property
    def dashboards(self) -> dict:
        return self._dashboards

    def add_dashboard(self, dashboard: Dashboard) -> Dashboard:
        self._dashboards[dashboard.id] = dashboard
        return dashboard

    def get_dashboard(self, dashboard_id: str) -> Dashboard:
        return self._dashboards[dashboard_id]

    def delete_dashboard(self, dashboard_id: str) -> None:
        del self._dashboards[dashboard_id]

    # Filters
    """
    Filters are system-level entities; they are registered
    when the torchlite app starts up.  Dashboards obtain the list of
    available filters from the app, and should present to the user only
    filters that have been registered.
    """

    @property
    def filters(self) -> dict[str, Callable]:
        return self.filter_factory.registry

    def register_filter(self, key: str, fn: Callable) -> None:
        self.filter_factory.register(key, fn)

    def get_filter(self, key: str) -> Callable:
        return self.filter_factory.registry[key]

    def delete_filter(self, key: str) -> None:
        del self.filter_factory.registry[key]
