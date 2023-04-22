import pytest

from htrc.ef.api import Api
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.widgets import TimeLineWidget
from htrc.torchlite.worksets import Workset


@pytest.fixture
def workset() -> Workset:
    ws = Workset("6416163a2d0000f9025c8284", Api())
    return ws


@pytest.fixture
def dashboard(workset: Workset) -> Dashboard:
    d = Dashboard()
    d.workset = workset
    return d


def test_dashboard(dashboard: Dashboard, workset: Workset) -> None:
    assert dashboard.workset == workset
    assert dashboard.widgets == {}
    widget = TimeLineWidget()
    dashboard.add_widget(widget)
    assert len(dashboard.widgets) == 1
