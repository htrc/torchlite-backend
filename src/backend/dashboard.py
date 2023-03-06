# -*- coding: utf-8 -*-
"""
The Torchlite backend Dashboard module.


Users interact with Torchlite via a dashboard
"""


import uuid
from backend.filters import FilterFactory


class Dashboard:
    def __init__(self, id=None):
        if id == None:
            self._id = uuid.uuid1()
        else:
            self._id = id
        self._widgets = {}
        self._workset = None
        self._token_data = None
        self._token_filters = set()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def reset_token_data(self):
        self._token_data = None

    def reset_data(self):
        self.reset_token_data()

    @property
    def id(self):
        return str(self._id)

    @property
    def widgets(self):
        return self._widgets

    @property
    def workset(self):
        return self._workset

    @workset.setter
    def workset(self, workset):
        self._workset = workset
        self.reset_data()
        for key in self.widgets:
            widget = self.get_widget(key)
            widget.workset = workset

    @property
    def token_filters(self):
        return self._token_filters

    @token_filters.setter
    def token_filters(self, filter_list):
        filter_set = set(filter_list)
        if self._token_filters != filter_set:
            self.reset_token_data()
            self._token_filters = filter_set

    @property
    def tokens(self):
        if not self._token_data:
            self._token_data = self.filter(list(self.workset.tokens.keys()))
        return self._token_data

    def filter(self, tokens):
        if self._token_filters == set():
            return tokens
        else:
            factory = FilterFactory()
            filter = factory.make_filter(self._token_filters)
            return filter.apply(tokens)

    def add_widget(self, widget):
        """Adds a widget to the dashboard."""
        widget.workset = self.workset
        self.widgets[str(widget.id)] = widget
        return self.widgets

    def get_widget(self, widget_id):
        """Returns the widget."""
        return self.widgets[widget_id]

    def delete_widget(self, widget_id):
        """Removes the widget from the dashboard."""
        del self.widgets[widget_id]
        return self.widgets
