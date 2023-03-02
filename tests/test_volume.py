import pytest
from htrc.torchlite.ef.volume import Volume


@pytest.fixture
def volume1():
    v = Volume("uc1.32106011187561")
    return v


@pytest.fixture
def volume2():
    v = Volume('loc.ark+=13960=t46q23w14')
    return v


def test_title(volume1):
    assert volume1.title == "Bilder vom Erzählen : Gedichte /"


def test_title2(volume2):
    assert volume2.title == 'Report of the historian for the year 19'


def test_type(volume1):
    assert 'Book' in volume1.type


def test_contributor(volume2):
    assert volume2.contributor['name'] == "Groton Historical Society (Groton, Mass.)"


def test_fetch_feature(volume1):
    result = volume1.fetch_feature('pageCount')
    assert result == 70
