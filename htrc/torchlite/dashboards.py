# -*- coding: utf-8 -*-
import uuid
from typing import Counter, Union


from htrc.torchlite.widgets import Widget
from htrc.torchlite.worksets import Workset


class Dashboard:
    def __init__(self) -> None:
        self.id: str = str(uuid.uuid1())
        self.widgets: dict = {}
        self._workset: Union[Workset, None] = None
        self.token_data: Union[Counter, None] = None
        self.token_filters: set = set()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    @property
    def info(self) -> dict:
        props: dict = {}
        props["id"] = self.id
        if self._workset:
            props["workset"] = self._workset.id
        if self.widgets:
            props["widgets"] = self.widgets
        return props

    def reset_token_data(self) -> None:
        self.token_data = None

    def reset_data(self) -> None:
        self.reset_token_data()

    @property
    def workset(self) -> Union[Workset, None]:
        return self._workset

    @workset.setter
    def workset(self, workset: Workset) -> None:
        self._workset = workset
        self.reset_data()

    def add_widget(self, widget: Widget) -> None:
        self.widgets[widget.id] = widget

    def get_widget(self, widget_id: str) -> Widget:
        return self.widgets[widget_id]

    def delete_widget(self, widget_id: str) -> None:
        del self.widgets[widget_id]
