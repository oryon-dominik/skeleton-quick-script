import pytest

from .. import __version__

@pytest.fixture
def version():
    yield __version__
