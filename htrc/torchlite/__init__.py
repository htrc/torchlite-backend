# -*- coding: utf-8 -*-
from htrc.ef.api import Api
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.filters import FilterFactory
from htrc.torchlite.widgets import Widget


class Torchlite:
    def __init__(self, ef_api: Api) -> None:
        self.ef_api = ef_api
        self._dashboards = {}
        self.widgets = {w.__name__: w for w in Widget.__subclasses__()}
        self.worksets = []
        self._filters = {}
        self.filter_factory = FilterFactory()

    def info(self):
        return {"dashboards": self._dashboards, "widgets": self.widgets}

    def add_workset(self, **kwargs):
        self.worksets.append(kwargs)

    @property
    def dashboards(self):
        return self._dashboards

    def add_dashboard(self, dashboard: Dashboard):
        self._dashboards[dashboard.id] = dashboard
        return dashboard

    def get_dashboard(self, dashboard_id):
        return self._dashboards[dashboard_id]

    def delete_dashboard(self, dashboard_id):
        del self._dashboards[dashboard_id]

    # Filters
    """
    Filters are system-level entities; they are registered
    when the torchlite app starts up.  Dashboards obtain the list of
    available filters from the app, and should present to the user only
    filters that have been registered.
    """

    @property
    def filters(self):
        return self.filter_factory.registry

    def register_filter(self, key, fn):
        self.filter_factory.register(key, fn)

    def get_filter(self, key):
        return self.filter_factory.registry[key]

    def delete_filter(self, key):
        del self.filter_factory.registry[key]
