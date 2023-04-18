import pytest
from htrc.ef.api import Api
from htrc.torchlite.worksets import Workset
from htrc.torchlite.widgets.projectors import TimeLineProjector

wsid = "6416163a2d0000f9025c8284"


def test_tlp():
    ws = Workset(wsid, Api())
    projector = TimeLineProjector()
    projector.project(ws)
    projection = projector.projection
    assert len(projection) == 4
    assert projection[0]['htid'] == 'mdp.35112103187797'
    assert projector.projection[0]['pubDate'] == 1947
