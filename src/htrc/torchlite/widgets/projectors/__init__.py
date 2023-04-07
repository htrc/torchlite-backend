from htrc.ef.datamodels import Workset
from htrc.ef import WorksetEndPoint
from htrc.torchlite import widgets


class Projector:
    def __init__(self, workset: Workset) -> None:
        self.workset = workset
        self.projection = None

    def project(self, workset, **kwargs):
        pass


class TimeLineProjector(Projector):
    def __init__(self, workset: Workset) -> None:
        super().__init__(workset)

    def project(self, **kwargs):
        endpoint = WorksetEndPoint()
        data = endpoint.get_metadata(self.workset.id, 'htid', 'metadata.pubDate')
        self.projection = [
            {'htid': d.htid, 'pubDate': d.metadata.pubDate} for d in data
        ]
        return self.projection
