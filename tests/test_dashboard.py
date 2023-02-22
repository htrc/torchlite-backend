import pytest
from backend.dashboard import Dashboard
from htrc.torchlite.ef import WorkSet, Volume
from backend.widgets import WidgetFactory
import uuid


@pytest.fixture
def workset():
    ws = WorkSet()
    ws.add_volume("loc.ark+=13960=t46q23w14")
    return ws


@pytest.fixture
def widget():
    return WidgetFactory.make_widget('MetadataWidget')


def test_dashboard_id():
    my_id = "foo"
    dashboard = Dashboard(my_id)
    assert dashboard.id == my_id

    dashboard2 = Dashboard()
    assert isinstance(dashboard2.id, str)


def test_dashboard(workset, widget):
    dashboard = Dashboard()
    assert dashboard.widgets == {}
    dashboard.add_widget(widget)
    assert dashboard.widgets[str(widget.id)] == widget
