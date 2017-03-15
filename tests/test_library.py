import pytest

import library
import exceptions


def test_retrieve_all_states(retrieved_states, correct_states):
    assert retrieved_states == correct_states


def test_retrieve_request_error_on_getting_all_states(bad_url):
    with pytest.raises(exceptions.RequestsError):
        library.get_all_states()


@pytest.fixture
def retrieved_states(get_patch, get_all_states_patch):
    states = library.get_all_states()
    return states


@pytest.fixture
def bad_url(monkeypatch):
    def url_mock():
        return 'FFFUUU!'

    monkeypatch.setattr(library, 'GET_ALL_STATES_URL', url_mock)
