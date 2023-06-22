from app.services.ef_api import EFApi
from app.models.torchlite import Workset
from app.widgets import MapWidget


def test_widget() -> None:
    workset = Workset("6416163a2d0000f9025c8284")
    widget = MapWidget(workset)
    assert widget.workset == workset
    data = list(widget.data())

    assert data[0]["pob"] == "http://www.wikidata.org/entity/Q23298"
    assert data[0]["pobLabel"] == "Kent"
    assert data[0]["coordinates"] == "Point(0.73 51.19)"
