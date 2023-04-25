from typing import Any, List
from htrc.torchlite.worksets import Workset


class Projector:
    def __init__(self) -> None:
        self.projection: List = []

    def project(self, workset: Workset) -> List:
        return []


class TimeLineProjector(Projector):
    def __init__(self) -> None:
        super().__init__()

    def project(self, workset: Workset) -> List[Any]:
        data = workset.metadata(["htid", "metadata.pubDate"])
        if data:
            self.projection = [{"htid": d.htid, "pubDate": d.metadata.pubDate} for d in data]
        else:
            self.projection = []
        return self.projection
