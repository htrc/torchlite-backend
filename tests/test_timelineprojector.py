import pytest
from htrc.ef import WorksetEndPoint
from htrc.torchlite.widgets.projectors import TimeLineProjector

wsid = "6416163a2d0000f9025c8284"


def test_tlp():
    ep = WorksetEndPoint()
    ws = ep.get_workset(wsid)
    projector = TimeLineProjector(ws)
    projection = projector.projection
    assert len(projection) == 4
    assert projection[0]['htid'] == 'mdp.35112103187797'
    assert projector.projection[0]['pubDate'] == 1947
