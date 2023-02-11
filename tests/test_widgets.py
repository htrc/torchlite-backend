import pytest
from torchlitelib.extracted_features import WorkSet
from backend.widgets import WidgetFactory
import json


@pytest.fixture
def workset():
    ws = WorkSet()
    ws.description = "minimal workset"
    [
        ws.add_volume(v_id)
        for v_id in ["uc1.32106011187561", "mdp.35112103187797", "uc1.$b684263"]
    ]
    return ws


def test_metadata_widget(workset):
    w = WidgetFactory.make_widget('MetadataWidget')
    data = w.apply_to(workset)
    assert len(data) == 3
