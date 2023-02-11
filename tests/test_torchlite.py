import pytest
from backend.torchlite import TorchLite
from backend.dashboard import Dashboard
from torchlitelib.extracted_features import Volume, WorkSet
from backend.widgets import WidgetFactory


@pytest.fixture
def volume_1():
    v = Volume("uc1.32106011187561")
    return v


@pytest.fixture
def volume_2():
    return Volume("loc.ark+=13960=t46q23w14")


@pytest.fixture
def workset_1(volume_1, volume_2):
    ws = WorkSet()
    ws.add_volume(Volume("uc1.32106011187561"))
    ws.add_volume(Volume("loc.ark+=13960=t46q23w14"))
    ws.description = "two volumes"
    return ws


@pytest.fixture
def widget_1():
    return WidgetFactory.make_widget('MetadataWidget')


def test_worksets(workset_1):
    torchlite = TorchLite()
    assert torchlite.worksets == {}
    torchlite.add_workset(workset_1)
    key = workset_1.id
    assert torchlite.get_workset(key) == workset_1
    assert len(torchlite.worksets) == 1


def test_dashboards():
    torchlite = TorchLite()
    assert len(torchlite.dashboards) == 0
    d = Dashboard()
    torchlite.add_dashboard(d)
    assert torchlite.get_dashboard(d.id) == d
    assert len(torchlite.dashboards) == 1
    torchlite.delete_dashboard(d.id)
    assert len(torchlite.dashboards) == 0


def test_add_workset_to_torchlite(workset_1):
    torchlite = TorchLite()
    torchlite.add_workset(workset_1)
    assert len(torchlite.worksets) == 1


def test_get_workset_to_torchlite(workset_1):
    torchlite = TorchLite()
    id = workset_1.id
    torchlite.add_workset(workset_1)
    assert torchlite.get_workset(id) == workset_1


def test_add_workset_to_torchlite(workset_1):
    torchlite = TorchLite()
    torchlite.add_workset(workset_1)
    assert len(torchlite.worksets) == 1


def test_add_workset_to_dashboard(workset_1):
    d = Dashboard()
    d.workset = workset_1
    assert d.workset == workset_1


def test_add_widget_to_dashboard(widget_1):
    d = Dashboard()
    d.add_widget(widget_1)
    assert len(d.widgets) == 1
