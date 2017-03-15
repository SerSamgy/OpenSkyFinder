import pytest

import library
import exceptions


def test_retrieve_all_states(retrieved_states, correct_states):
    assert retrieved_states == correct_states


def test_retrieve_request_error_on_getting_all_states(bad_url):
    with pytest.raises(exceptions.RequestsError):
        library.get_all_states()
        
        
def test_distance_between_points(retrieved_distance, correct_distance):
    assert retrieved_distance == correct_distance


def test_get_vehicle_information(vehicle_info_gen, vehicle_1, vehicle_2):
    assert next(vehicle_info_gen) == vehicle_1
    assert next(vehicle_info_gen) == vehicle_2


@pytest.fixture
def retrieved_states(get_patch, get_all_states_patch):
    states = library.get_all_states()
    return states


@pytest.fixture
def bad_url(monkeypatch):
    def url_mock():
        return 'FFFUUU!'

    monkeypatch.setattr(library, 'GET_ALL_STATES_URL', url_mock)


@pytest.fixture
def paris():
    return 48.8567, 2.3508


@pytest.fixture
def tours():
    return 47.394144, 0.68484


@pytest.fixture
def retrieved_distance(paris, tours):
    return round(library.distance_between_points(paris, tours))


@pytest.fixture
def correct_distance():
    return 204


@pytest.fixture
def vehicle_info_gen(correct_states):
    return library.get_vehicle_with_coordinates(correct_states['states'])
