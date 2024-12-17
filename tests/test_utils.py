from htrc.torchlite.utils import flatten


def test_flatten():
    assert flatten([]) == []
    assert flatten([[]]) == []
    assert flatten([[1, 2, 3]]) == [1, 2, 3]
    assert flatten([[1, 2, 3], [4, 5], [6]]) == [1, 2, 3, 4, 5, 6]
