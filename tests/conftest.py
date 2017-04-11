import pytest
import requests

from skyfinder import methods

all_states = {
    "time": 1489568690,
    "states": [
        ["aab276", "FDX1166 ", "United States", 1489568688, 1489568688,
         -102.3371, 35.8629, 11582.4, False, 225.85, 306.48, 0, None,
         11582.4, None, False, False],
        ["89906e", "EVA218  ", "Taiwan", 1489568686, 1489568686, 120.4294,
         24.1535, 6271.26, False, 189.05, 17.74, -8.78, None, 6271.26,
         None, False, False],
        ["3450d7", "IBE6800 ", "Spain", 1489592518, 1489592518, -0.1487,
         44.7269, 11887.2, False, 233.48, 210.01, 0.33, None, 11887.2, None,
         False, False],
        ["3b7776", "CHEPTELA", "France", 1489592519, 1489592519, 3.1881,
         46.1673, 8382, False, None, None, None, None, 8382, None, False, False],
        ["3c7d87", "HOP15GC ", "Germany", 1489592519, 1489592519, None,
         None, 10050.78, False, 212.57, 196.59, 0, None, 10050.78, None,
         False, False]
    ]
}


@pytest.fixture
def correct_states():
    return all_states


@pytest.fixture
def available_vehicles(correct_states):
    vehicles = []

    for vehicle in correct_states['states']:
        vehicle_item = methods.Vehicle(vehicle[1], (vehicle[6], vehicle[5]))
        vehicles.append(vehicle_item)

    return vehicles


@pytest.fixture
def close_vehicle_from_spain(available_vehicles):
    return available_vehicles[2].callsign


@pytest.fixture
def close_vehicle_from_france(available_vehicles):
    return available_vehicles[3].callsign


@pytest.fixture
def correct_vehicles_in_radius(close_vehicle_from_spain, close_vehicle_from_france):
    return [close_vehicle_from_spain, close_vehicle_from_france]


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
