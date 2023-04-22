from typing import Any, List, Tuple, Union
from htrc.torchlite.worksets import Workset


class Projector:
    def __init__(self) -> None:
        self.projection: Union[List, None] = None

    def project(self, workset: Workset) -> List:
        return []


class TimeLineProjector(Projector):
    def __init__(self) -> None:
        super().__init__()

    def project(self, workset: Workset) -> List[Any]:
        data = workset.metadata(["htid", "metadata.pubDate"])
        self.projection = [{"htid": d.htid, "pubDate": d.metadata.pubDate} for d in data]
        return self.projection
