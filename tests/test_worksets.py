from app.services.ef_api import EFApi
from app.models.torchlite import Workset


def test_workset() -> None:
    ws = Workset("6416163a2d0000f9025c8284")
    assert ws.volumes and len(ws.volumes) == 4
