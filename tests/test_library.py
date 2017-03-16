import pytest

from src import skyfinder, exceptions

paris_coordinates = (48.8567, 2.3508)
radius_and_error = (450, 50)


def test_retrieve_all_states(retrieved_states, correct_states):
    assert retrieved_states == correct_states


def test_retrieve_request_error_on_getting_all_states(bad_url):
    with pytest.raises(exceptions.RequestsError):
        skyfinder.get_all_states()
        
        
def test_distance_between_points(retrieved_distance, correct_distance):
    assert retrieved_distance == correct_distance


def test_get_vehicle_information(vehicle_info_gen, available_vehicles):
    for retrieved, correct in zip(vehicle_info_gen, available_vehicles):
        assert retrieved == correct


def test_check_if_vehicle_in_radius(vehicle_check_result, vehicle_check_correct):
    assert vehicle_check_result == vehicle_check_correct


def test_retrieve_all_vehicles_in_radius(vehicles_in_radius, correct_vehicles_in_radius):
    assert vehicles_in_radius == correct_vehicles_in_radius


@pytest.fixture
def retrieved_states(get_patch, get_all_states_patch):
    states = skyfinder.get_all_states()
    return states


@pytest.fixture
def bad_url(monkeypatch):
    def url_mock():
        return 'FFFUUU!'

    monkeypatch.setattr(skyfinder, 'GET_ALL_STATES_URL', url_mock)


@pytest.fixture
def paris():
    return paris_coordinates


@pytest.fixture
def tours():
    return 47.394144, 0.68484


@pytest.fixture
def retrieved_distance(paris, tours):
    return round(skyfinder.distance_between_points(paris, tours))


@pytest.fixture
def correct_distance():
    return 204


@pytest.fixture
def vehicle_info_gen(correct_states):
    return skyfinder.get_vehicle_with_coordinates(correct_states['states'])


@pytest.fixture(params=[
    ((paris_coordinates, (47.3941, 0.68484), radius_and_error[0]), True),
    ((paris_coordinates, (51.9499, 6.43714), radius_and_error[0]), True),
    ((paris_coordinates, (51.9499, 6.53714), radius_and_error[0]), False),
    ((paris_coordinates, (50.7499, 6.63714), *radius_and_error), True),
    ((paris_coordinates, (51.9499, 6.43714), *radius_and_error), True),
    ((paris_coordinates, (51.9499, 6.73714), *radius_and_error), True),
    ((paris_coordinates, (52.6499, 6.73714), *radius_and_error), False)
], ids=[
    "vehicle is in distance less than radius without error",
    "vehicle is in distance equal to radius without error",
    "vehicle is in distance greater than radius without error",
    "vehicle is in distance less than radius with error",
    "vehicle is in distance equal to radius with error",
    "vehicle is in distance greater than radius with error",
    "vehicle is in distance greater than radius + error"
])
def check_if_vehicle_in_radius(request):
    return skyfinder.check_if_vehicle_in_radius(*request.param[0]), request.param[1]


@pytest.fixture
def vehicle_check_result(check_if_vehicle_in_radius):
    return check_if_vehicle_in_radius[0]


@pytest.fixture
def vehicle_check_correct(check_if_vehicle_in_radius):
    return check_if_vehicle_in_radius[1]


@pytest.fixture
def vehicles_in_radius(paris, correct_states):
    return skyfinder.retrieve_all_vehicles_in_radius(paris,
                                                     correct_states['states'],
                                                     *radius_and_error)
