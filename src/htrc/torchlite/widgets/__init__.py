from typing import Protocol, Union
import uuid

from pydantic import NoneStr
from htrc.ef.datamodels import Workset
from htrc.torchlite.widgets import projectors
from htrc.torchlite.widgets.projectors import Projector, TimeLineProjector


class Widget:
    def __init__(self, workset: Workset) -> None:
        self.id = uuid.uuid1()
        self._workset: Workset = workset
        self._projector: Union[Projector, None] = None
        self._cache = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    def reset(self) -> None:
        self._cache = None

    @property
    def workset(self) -> Union[Workset, None]:
        return self._workset

    @workset.setter
    def workset(self, workset: Workset) -> None:
        self._workset = workset
        if self._projector:
            self._projector.workset = workset
        self.reset()

    @property
    def data(self):
        if self._cache is None:
            if self._projector:
                self._cache = self._projector.projection
        return self._cache


class TimeLineWidget(Widget):
    '''publication timeline for workset'''

    def __init__(self, workset: Workset) -> None:
        super().__init__(workset)
        self._projector = TimeLineProjector(workset)


class WidgetFactory:
    def __init__(self):
        self._widget_classes = {}

    @classmethod
    def make_widget(cls, widget_class: str, ws=None):
        try:
            klass = globals()[widget_class]
            widget = klass(ws)
            return widget
        except KeyError:
            print(f"Widget class {widget_class} not defined")
            raise KeyError()
