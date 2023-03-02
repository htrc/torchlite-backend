import pytest
from htrc.torchlite.ef.workset import WorkSet
from htrc.torchlite.ef.page import Page


@pytest.fixture
def workset():
    ws = WorkSet('63f7ae452500006404fc54c7')
    return ws


def test_volumes(workset):
    assert len(workset.volumes) == 4
