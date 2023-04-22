from htrc.ef.api import Api
from htrc.torchlite.widgets.projectors import TimeLineProjector
from htrc.torchlite.worksets import Workset

wsid: str = "6416163a2d0000f9025c8284"


def test_tlp() -> None:
    ef_api: Api = Api()
    ws: Workset = Workset(wsid, ef_api)
    projector = TimeLineProjector()
    projector.project(ws)
    projection = projector.projection
    assert len(projection) == 4
    assert projection[0]["htid"] == "mdp.35112103187797"
    assert projector.projection[0]["pubDate"] == 1947
