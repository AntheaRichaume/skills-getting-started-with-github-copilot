from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities_state():
    original_activities = deepcopy(app_module.activities)
    app_module.activities = deepcopy(original_activities)
    yield
    app_module.activities = deepcopy(original_activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)