from typing import Protocol, Union
import uuid

from pydantic import NoneStr
from htrc.ef.datamodels import Workset
from htrc.torchlite.widgets.projectors import Projector, TimeLineProjector


class Widget:
    def __init__(self, workset: Workset) -> None:
        self.id = str(uuid.uuid1())
        self.projector: Union[Projector, None] = None
        self.workset = workset
        self._cache = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    def reset(self) -> None:
        self._cache = None

    # @property
    # def workset(self) -> Union[Workset, None]:
    #     return self.dashboard.workset

    # @workset.setter
    # def workset(self, workset: Workset) -> None:
    #     self._workset = workset
    #     self.reset()

    @property
    def data(self):
        if self._cache is None:
            self.projector.project()
            self._cache = self.projector.projection
        return self._cache


class TimeLineWidget(Widget):
    '''publication timeline for workset'''

    def __init__(self, workset: Workset) -> None:
        super().__init__(workset)
        self.projector = TimeLineProjector(self.workset)
