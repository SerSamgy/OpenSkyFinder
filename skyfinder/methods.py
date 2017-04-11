"""
A collection of methods to work with OpenSky API.
"""

import collections

import requests
from haversine import haversine

import skyfinder.exceptions as exceptions

OPEN_SKY_URL = 'https://opensky-network.org/api'
GET_ALL_STATES_URL = OPEN_SKY_URL + '/states/all'
Vehicle = collections.namedtuple('Vehicle', 'callsign, coordinates')


def get_all_states():
    """Get all states from OpenSky site.

    :return: json data
    :rtype: dict
    :raises: exceptions.RequestException
    """
    try:
        response = requests.get(GET_ALL_STATES_URL)
    except requests.RequestException as exc:
        raise exceptions.RequestsError(exc) from exc

    return response.json()


def get_vehicle_with_coordinates(states):
    """Get vehicle call sign with its coordinates.

    :param states: List of lists with vehicles states
    :return: Vehicle object
    """
    for item in states:
        if item[1] and item[5] and item[6]:
            yield Vehicle(item[1], (item[6], item[5]))


def check_if_vehicle_in_radius(origin, coordinates, radius, error=None):
    """Check if vehicle is in radius of origin point.

    :param origin: Coordinates of point to check radius from in format 'latitude, longitude'
    :param coordinates: Coordinates of vehicle in format 'latitude, longitude'
    :param radius: Integer value of radius in kilometers from origin point.
    :param error: (optional) Integer value for measurement error
    :return: bool
    """
    if error:
        max_err_distance = radius + error
        if distance_between_points(origin, coordinates) <= max_err_distance:
            return True

    if distance_between_points(origin, coordinates) <= radius:
        return True

    return False


def retrieve_all_vehicles_in_radius(origin, states, radius, error=None):
    """Get generator of vehicles call signs which are in radius of origin point.

    :param origin: Coordinates of point to check radius from in format 'latitude, longitude'
    :param states: List of lists with vehicles states
    :param radius: Integer value of radius in kilometers from origin point.
    :param error: (optional) Integer value for measurement error
    :return: generator object of vehicles call signs

    Example. Find all vehicles within a radius of 450 kilometers from Paris (±50 km)::

    >>> paris_coordinates = (48.8567, 2.3508)
    >>> radius_and_error = (450, 50)
    >>> states = [\
        ["aab276", "FDX1166 ", "United States", 1489568688, 1489568688,\
         -102.3371, 35.8629, 11582.4, False, 225.85, 306.48, 0, None,\
         11582.4, None, False, False],\
        ["89906e", "EVA218  ", "Taiwan", 1489568686, 1489568686, 120.4294,\
         24.1535, 6271.26, False, 189.05, 17.74, -8.78, None, 6271.26,\
         None, False, False],\
        ["3450d7", "IBE6800 ", "Spain", 1489592518, 1489592518, -0.1487,\
         44.7269, 11887.2, False, 233.48, 210.01, 0.33, None, 11887.2, None,\
         False, False],\
        ["3b7776", "CHEPTELA", "France", 1489592519, 1489592519, 3.1881,\
         46.1673, 8382, False, None, None, None, None, 8382, None, False, False],\
        ["3c7d87", "HOP15GC ", "Germany", 1489592519, 1489592519, None,\
         None, 10050.78, False, 212.57, 196.59, 0, None, 10050.78, None,\
         False, False]\
    ]
    >>> list(retrieve_all_vehicles_in_radius(paris_coordinates, states, *radius_and_error))
    ['IBE6800 ', 'CHEPTELA']
    """

    for vehicle in get_vehicle_with_coordinates(states):
        if check_if_vehicle_in_radius(origin, vehicle.coordinates, radius, error):
            yield vehicle.callsign


def distance_between_points(point1, point2):
    """Get distance between points in km.

    :param point1: tuple in format 'latitude, longitude'
    :param point2: tuple in format 'latitude, longitude'
    :return: float number
    """
    return haversine(point1, point2)
