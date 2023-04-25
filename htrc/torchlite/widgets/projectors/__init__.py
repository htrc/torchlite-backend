from typing import Any, List
from htrc.torchlite.worksets import Workset
import htrc.ef.datamodels as ef


class Projector:
    def __init__(self) -> None:
        self.projection: List = []

    def project(self, workset: Workset) -> List:
        return []


class TimeLineProjector(Projector):
    def __init__(self) -> None:
        super().__init__()

    def project(self, workset: Workset) -> List[Any]:
        data: List[ef.Volume] | None = workset.metadata(["htid", "metadata.pubDate"])
        if data:
            self.projection = [{"htid": vol.htid, "pubDate": vol.metadata.pubDate} for vol in data]
        return self.projection
