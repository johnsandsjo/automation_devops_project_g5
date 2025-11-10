import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from weather_app.app import app 

@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()
