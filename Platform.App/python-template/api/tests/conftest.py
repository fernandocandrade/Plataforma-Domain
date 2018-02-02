# conftest.py
import pytest
from api.server import app as _app


@pytest.fixture
def app():
    _app.debug = True
    _app.testing = True
    return _app