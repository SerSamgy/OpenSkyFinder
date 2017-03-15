from haversine import haversine
import requests

import exceptions

OPEN_SKY_URL = 'https://opensky-network.org/api'
GET_ALL_STATES_URL = OPEN_SKY_URL + '/states/all'


def get_all_states():
    try:
        response = requests.get(GET_ALL_STATES_URL)
    except requests.RequestException as exc:
        raise exceptions.RequestsError(exc) from exc

    return response.json()


def get_vehicle_with_coordinates(states):
    for item in states:
        yield item[1], (item[6], item[5])  # callsign, (lat, long)


def check_if_vehicle_in_radius(origin, vehicle, radius, error=None):
    if error:
        max_err_distance = radius + error
        if distance_between_points(origin, vehicle) <= max_err_distance:
            return True

    if distance_between_points(origin, vehicle) <= radius:
        return True

    return False


def distance_between_points(point1, point2):
    return haversine(point1, point2)
