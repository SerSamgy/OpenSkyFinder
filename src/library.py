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
