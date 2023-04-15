# -*- coding: utf-8 -*-
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.widgets import Widget
from htrc.torchlite.filters import FilterFactory
from htrc.ef.datamodels import Workset


class Torchlite:
    def __init__(self) -> None:
        self._dashboards = []
        self._widgets = {w.__name__: w for w in Widget.__subclasses__()}
        self._worksets = []
        self._filters = {}
        self.filter_factory = FilterFactory()

    def info(self):
        info = {}
        info["worksets"] = [
            {"id": ws['workset'].id, "description": ws['description']}
            for ws in self._worksets
        ]
        info['dashboards'] = []
        for d in self._dashboards:
            db = d['dashboard']
            # timestamp = d['timestamp']
            info['dashboards'].append(
                {
                    'id': db.id,
                    # 'timestamp': timestamp,
                    'workset': db.workset.id,
                    'widgets': db.widgets,
                }
            )
        info['registered_widgets'] = self.widgets

        return info

    @property
    def worksets(self):
        return self._worksets

    def add_workset(self, workset: Workset, **kwargs):
        entry = {"workset": workset, **kwargs}
        self._worksets.append(entry)

    def get_workset(self, workset_id: str):
        return next(filter(lambda x: x['workset'].id == workset_id, self._worksets))

    def delete_workset(self, workset_id: str) -> None:
        ws = self.get_workset(workset_id)
        if ws:
            self._worksets.remove(ws)

    @property
    def dashboards(self):
        return self._dashboards

    def add_dashboard(self, dashboard: Dashboard, **kwargs):
        # dashboard.filter_factory = self.filter_factory
        entry = {"dashboard": dashboard, **kwargs}
        self._dashboards.append(entry)

    def get_dashboard(self, dashboard_id):
        return next(
            filter(lambda x: x['dashboard'].id == dashboard_id, self.dashboards)
        )

    def delete_dashboard(self, dashboard_id):
        dashboard = self.get_dashboard(dashboard_id)
        if dashboard:
            self._dashboards.remove(dashboard)

    @property
    def widgets(self):
        '''The list of registered widgets'''
        return self._widgets

    # def add_widget(self, widget):
    #     self.widgets[str(widget.id)] = widget
    #     return self.widgets

    def get_widget(self, widget_id):
        return self.widgets[widget_id]

    def delete_widget(self, widget_id):
        del self.widgets[widget_id]
        return self.widgets

    # Filters
    '''
    Filters are system-level entities; they are registered
    when the torchlite app starts up.  Dashboards obtain the list of
    available filters from the app, and should present to the user only
    filters that have been registered.
    '''

    @property
    def filters(self):
        return self.filter_factory.registry

    def register_filter(self, key, fn):
        self.filter_factory.register(key, fn)

    def get_filter(self, key):
        return self.filter_factory.registry[key]

    def delete_filter(self, key):
        del self.filter_factory.registry[key]
