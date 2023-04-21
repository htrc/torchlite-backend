from htrc.torchlite.worksets import Workset


class Projector:
    def __init__(self) -> None:
        self.projection = None

    def project(self, workset: Workset):
        pass


class TimeLineProjector(Projector):
    def __init__(self) -> None:
        super().__init__()

    def project(self, workset: Workset):
        data = workset.metadata(['htid', 'metadata.pubDate'])
        self.projection = [
            {'htid': d.htid, 'pubDate': d.metadata.pubDate} for d in data
        ]
        return self.projection
