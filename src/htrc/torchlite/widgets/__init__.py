from typing import Protocol, Union
import uuid
from pydantic import NoneStr
from htrc.torchlite.worksets import Workset
import htrc.ef.datamodels as ef
from htrc.torchlite.widgets.projectors import Projector, TimeLineProjector


class Widget:
    def __init__(self) -> None:
        self.id = str(uuid.uuid1())
        self.dashboard: "Dashboard"
        self.projector: Projector
        self._cache = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    def reset(self) -> None:
        self._cache = None

    @property
    def workset(self) -> Workset:
        return self.dashboard.workset

    @property
    def data(self):
        if self._cache is None:
            self.projector.project(self.workset)
            self._cache = self.projector.projection
        return self._cache


class TimeLineWidget(Widget):
    '''publication timeline for workset'''

    def __init__(self) -> None:
        super().__init__()
        self.projector = TimeLineProjector()
