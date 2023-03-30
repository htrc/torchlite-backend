from htrc.ef.datamodels import Workset
from htrc.ef import WorksetEndPoint


class Projector:
    def __init__(self, workset) -> None:
        self.workset = workset
        self._projection = None

    def generate_projection(self, **kwargs):
        pass

    @property
    def projection(self):
        if self._projection is None:
            self._projection = self.generate_projection()
        return self._projection


class TimeLineProjector(Projector):
    def __init__(self, workset) -> None:
        super().__init__(workset)

    def generate_projection(self, **kwargs):
        endpoint = WorksetEndPoint()
        data = endpoint.get_metadata(self.workset.id, 'htid', 'metadata.pubDate')
        return [{'htid': d.htid, 'pubDate': d.metadata.pubDate} for d in data]
