import pytest
from htrc.torchlite.ef import WorkSet, Page


@pytest.fixture
def workset():
    mini_workset = WorkSet()

    mini_workset.add_volume("uc1.32106011187561")
    mini_workset.add_volume("mdp.35112103187797")
    mini_workset.add_volume("uc1.$b684263")
    mini_workset.description = "minimal workset"
    return mini_workset


def test_volumes(workset):
    assert len(workset.volumes) == 3
