# -*- coding: utf-8 -*-
import uuid
from typing import Union

from pydantic import UUID1

from htrc.torchlite.widgets import Widget
from htrc.torchlite.worksets import Workset


class Dashboard:
    def __init__(self) -> None:
        self.id = str(uuid.uuid1())
        self.widgets = {}
        self._workset: Union[Workset, None] = None
        self.token_data = None
        self.token_filters = set()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    @property
    def info(self):
        props = {}
        props['id'] = self.id
        if self._workset:
            props['workset'] = self._workset.id
        if self.widgets:
            props['widgets'] = self.widgets
        return props

    def reset_token_data(self):
        self.token_data = None

    def reset_data(self):
        self.reset_token_data()

    @property
    def workset(self) -> Union[Workset, None]:
        return self._workset

    @workset.setter
    def workset(self, workset: Workset):
        self._workset = workset
        self.reset_data()

    def add_widget(self, widget: Widget):
        self.widgets[widget.id] = widget

    def get_widget(self, widget_id: UUID1):
        return self.widgets[widget_id]

    def delete_widget(self, widget_id: UUID1):
        del self.widgets[widget_id]
