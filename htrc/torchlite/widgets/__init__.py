import uuid
from typing import Any, List, Optional, Union
from htrc.torchlite.widgets.projectors import Projector, TimeLineProjector
from htrc.torchlite.worksets import Workset

class Widget:
    def __init__(self) -> None:
        self.id: str = str(uuid.uuid1())
        self.projector: Projector
        self._cache: Optional[List[Any]] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    def reset(self) -> None:
        self._cache = None

    def get_data(self, workset: Optional[Workset]) -> Union[List[Any], None]:
        if self._cache is None:
            if workset:
                self.projector.project(workset)
                self._cache = self.projector.projection
        return self._cache


class TimeLineWidget(Widget):
    """publication timeline for workset"""

    def __init__(self) -> None:
        super().__init__()
        self.projector = TimeLineProjector()
