from copy import deepcopy
from importlib import import_module

import pytest
from fastapi.testclient import TestClient

app_module = import_module("src.app")


@pytest.fixture
def activity_data(monkeypatch):
    data = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Basketball Team": {
            "description": "Practice basketball skills and compete in games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": [],
        },
    }
    monkeypatch.setattr(app_module, "activities", deepcopy(data))
    return data


@pytest.fixture
def client(activity_data):
    with TestClient(app_module.app) as test_client:
        yield test_client
