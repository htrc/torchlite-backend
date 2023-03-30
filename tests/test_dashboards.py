import pytest
from htrc.torchlite.dashboards import Dashboard
from htrc.torchlite.widgets import WidgetFactory, TimeLineWidget
from htrc.ef import WorksetEndPoint


@pytest.fixture
def workset():
    ws = WorksetEndPoint().get_workset('6416163a2d0000f9025c8284')
    return ws


@pytest.fixture
def dashboard(workset):
    return Dashboard(workset=workset)


@pytest.fixture
def widget(workset):
    return WidgetFactory.make_widget('TimeLineWidget', workset)


def test_dashboard(dashboard, workset, widget):
    assert dashboard.workset == workset
    assert dashboard.widgets == []
    dashboard.add_widget(widget)
    assert dashboard.get_widget(widget.id) == widget
    dashboard.delete_widget(widget.id)
    assert dashboard.widgets == []
