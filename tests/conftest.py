import pytest
import requests

all_states = {
    "time": 1489568690,
    "states": [
        ["aab276", "FDX1166", "United States", 1489568688, 1489568688,
         -102.3371, 35.8629, 11582.4, False, 225.85, 306.48, 0, None,
         11582.4, None, False, False],
        ["89906e", "EVA218", "Taiwan", 1489568686, 1489568686, 120.4294,
         24.1535, 6271.26, False, 189.05, 17.74, -8.78, None, 6271.26,
         None, False, False]
    ]
}


@pytest.fixture
def correct_states():
    return all_states


@pytest.fixture
def vehicle_1():
    return 'FDX1166', (35.8629, -102.3371)


@pytest.fixture
def vehicle_2():
    return 'EVA218', (24.1535, 120.4294)


@pytest.fixture
def get_patch(monkeypatch):
    def get_mock(url):
        return requests.Response()

    monkeypatch.setattr(requests, 'get', get_mock)


@pytest.fixture
def get_all_states_patch(monkeypatch):
    def all_states_mock(self):
        return all_states

    monkeypatch.setattr(requests.Response, 'json', all_states_mock)
