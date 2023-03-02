import pytest
from htrc.torchlite.ef.workset import WorkSet
from backend.widgets import WidgetFactory
import json


@pytest.fixture
def workset():
    ws = WorkSet('63f7ae452500006404fc54c7')
    return ws


def test_metadata_widget(workset):
    w = WidgetFactory.make_widget('MetadataWidget')
    data = w.apply_to(workset)
    assert len(data) == 4
