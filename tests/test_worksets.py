from htrc.ef.api import Api
from htrc.torchlite.worksets import Workset


def test_workset():
    ws = Workset("6416163a2d0000f9025c8284", Api())
    assert len(ws.volumes) == 4
