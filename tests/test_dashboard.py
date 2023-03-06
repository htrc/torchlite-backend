import pytest
from backend.dashboard import Dashboard
from htrc.torchlite.ef.workset import WorkSet
from htrc.torchlite.ef.volume import Volume
from backend.widgets import WidgetFactory
import uuid


@pytest.fixture
def workset():
    ws = WorkSet('63f7ae452500006404fc54c7')
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


def test_filters():
    dashboard = Dashboard()
    assert dashboard._token_filters == set()
    assert dashboard._token_data == None
    test_data = ['alpha', 'beta']
    dashboard._token_data = test_data
    dashboard.token_filters = ['a', 'b']
    assert dashboard._token_filters == set(['a', 'b'])
    assert dashboard._token_data == None
    dashboard._token_data = test_data
    dashboard.token_filters = ['a', 'b']
    assert dashboard._token_data == test_data
