import pytest
from backend.torchlite import TorchLite
from backend.dashboard import Dashboard
from htrc.torchlite.ef.workset import WorkSet
from htrc.torchlite.ef.volume import Volume
from backend.widgets import WidgetFactory

@pytest.fixture
def workset():
    ws = WorkSet('63f7ae452500006404fc54c7')
    return ws


@pytest.fixture
def widget_1():
    return WidgetFactory.make_widget('MetadataWidget')


def test_worksets(workset):
    torchlite = TorchLite()
    assert torchlite.worksets == {}
    torchlite.add_workset(workset)
    key = workset.htid
    assert torchlite.get_workset(key) == workset
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


def test_add_workset_to_torchlite(workset):
    torchlite = TorchLite()
    torchlite.add_workset(workset)
    assert len(torchlite.worksets) == 1


def test_get_workset_to_torchlite(workset):
    torchlite = TorchLite()
    id = workset.htid
    torchlite.add_workset(workset)
    assert torchlite.get_workset(id) == workset


def test_add_workset_to_torchlite(workset):
    torchlite = TorchLite()
    torchlite.add_workset(workset)
    assert len(torchlite.worksets) == 1


def test_add_workset_to_dashboard(workset):
    d = Dashboard()
    d.workset = workset
    assert d.workset == workset


def test_add_widget_to_dashboard(widget_1):
    d = Dashboard()
    d.add_widget(widget_1)
    assert len(d.widgets) == 1
