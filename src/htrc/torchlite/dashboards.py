# -*- coding: utf-8 -*-
import uuid
from typing import Union, List
from pydantic import UUID1
from htrc.torchlite.widgets import Widget
from htrc.torchlite.worksets import Workset


class Dashboard:
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid1())
        self._widgets: List[Widget] = []
        self._workset: Union[Workset, None] = None
        if 'workset' in kwargs:
            self._workset = kwargs['workset']
        self.token_data = None
        self.token_filters = set()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

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

    @property
    def widgets(self) -> List[Widget]:
        return self._widgets

    def add_widget(self, widget_class):
        widget = widget_class()
        widget.dashboard = self
        self.widgets.append(widget)

    def get_widget(self, widget_id: UUID1):
        return next(filter(lambda w: w.id == widget_id, self._widgets))

    def delete_widget(self, widget_id: UUID1):
        widget = self.get_widget(widget_id)
        self._widgets.remove(widget)
