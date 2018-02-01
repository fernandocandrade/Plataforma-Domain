# conftest.py
import pytest
from api.server import get_app


@pytest.fixture
def app():
    app = get_app()
    app.debug = True
    app.testing = True
    return app