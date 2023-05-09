from typing import Any, List, Optional
from htrc.torchlite.worksets import Workset
import htrc.ef.datamodels as ef


class WidgetError(Exception):
    """Widget error of some kind"""

    pass


class NotValidWidgetType(WidgetError):
    "specified type not found in registry"
    pass


class Widget:
    def __init__(self) -> None:
        self._cache: Optional[List[Any]] = None

    def reset(self) -> None:
        self._cache = None

    def projection(self, workset: Workset) -> List[Any] | None:
        pass


class TimeLineWidget(Widget):
    def __init__(self) -> None:
        super().__init__()

    def projection(self, workset: Workset) -> List[Any]:
        projection: List[Any] = []
        data: List[ef.Volume] | None = workset.metadata(["htid", "metadata.pubDate"])
        if data:
            projection = [{"htid": vol.htid, "pubDate": vol.metadata.pubDate} for vol in data]
        return projection


class WidgetFactory:
    def __init__(self) -> None:
        self.registry: dict[str, type[Widget]] = {}

    def register_widget(self, key: str, widget_class: type[Widget]) -> None:
        self.registry[key] = widget_class

    def make_widget(self, key: str) -> Widget:
        try:
            klass = self.registry[key]
            return klass()
        except NotValidWidgetType:
            print(f"{key} not found in widget factory registry")
            raise
