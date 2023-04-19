import pytest

from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.widgets import TimeLineWidget
from htrc.torchlite.worksets import Workset
from htrc.ef.api import Api


@pytest.fixture
def workset():
    ws = Workset('6416163a2d0000f9025c8284', Api())
    return ws


@pytest.fixture
def dashboard(workset):
    d = Dashboard()
    d.workset = workset
    return d


def test_dashboard(dashboard, workset):
    assert dashboard.workset == workset
    assert dashboard.widgets == []
    dashboard.add_widget(TimeLineWidget)
    assert len(dashboard.widgets) == 1
