# conftest.py
import pytest
from api.server import get_app


@pytest.fixture
def app():
    _app = get_app()
    _app.debug = True
    _app.testing = True
    return _app