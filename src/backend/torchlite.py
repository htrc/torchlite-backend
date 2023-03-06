from torchlitelib.extracted_features import WorkSet
from backend.dashboard import Dashboard
from backend.widgets import Widget


class TorchLite:
    def __init__(self):
        self._dashboards = {}
        self._widgets = {}
        self._worksets = {}
        self._filters = {}

        for cls in Widget.__subclasses__():
            self._widgets[cls.__name__] = cls.__doc__

    @property
    def dashboards(self):
        return [k for k in self._dashboards.keys()]

    def add_dashboard(self, dashboard):
        self._dashboards[str(dashboard.id)] = dashboard
        return self.dashboards

    def get_dashboard(self, dashboard_id):
        return self._dashboards[dashboard_id]

    def delete_dashboard(self, dashboard_id):
        del self._dashboards[dashboard_id]
        return self.dashboards

    @property
    def widgets(self):
        '''The list of registered widgets'''
        return self._widgets

    def add_widget(self, widget):
        self.widgets[str(widget.id)] = widget
        return self.widgets

    def get_widget(self, widget_id):
        return self.widgets[widget_id]

    def delete_widget(self, widget_id):
        del self.widgets[widget_id]
        return self.widgets

    @property
    def worksets(self):
        return self._worksets

    def add_workset(self, workset):
        self.worksets[str(workset.htid)] = workset
        return self.worksets

    def get_workset(self, workset_id):
        return self.worksets[workset_id]

    def delete_workset(self, workset_id):
        del self.worksets[workset_id]
        return self.worksets

    # Filters
    '''
    Filters are system-level entities; they are registered
    when the torchlite app starts up.  Dashboards obtain the list of
    available filters from the app, and should present to the user only
    filters that have been registered.
    '''

    @property
    def filters(self):
        return self._filters

    def register_filter(self, key, fn):
        self._filters[key] = fn

    def get_filter(self, key):
        return self._filters[key]

    def delete_filter(self, key):
        del self._filters[key]
