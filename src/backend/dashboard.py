# -*- coding: utf-8 -*-
"""
The Torchlite backend Dashboard module.


Users interact with Torchlite via a dashboard
"""


import uuid


class Dashboard:
    def __init__(self, id=None):
        if id == None:
            self._id = uuid.uuid1()
        else:
            self._id = id
        self._widgets = {}
        self._workset = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

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
        for key in self.widgets:
            widget = self.get_widget(key)
            widget.workset = workset

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
