import pytest

from func.src.service import TicketListService
from func.src.validator import Filter
from unittest.mock import patch, MagicMock
from zenpy import Zenpy


class StubZenpyUser:
    def __init__(self, values):
        self.values = values


class StubZenpy:
    def __init__(self, user):
        self.users_args = None
        self.user = user

    def users(self, *args, **kwargs):
        self.users_args = (args, kwargs)
        return self.user


@patch.object(TicketListService, '_get_zenpy_client')
def test_get_user(zenpy_users):
    stub_zenpy = StubZenpy(user=StubZenpyUser(values=[10]))
    TicketListService.zenpy_client = stub_zenpy
    zenpy_users.return_value = stub_zenpy
    client_ticket_list_service = TicketListService(
        url_path='',
        params=Filter(**{
            "page": 1,
            "page_size": 0
        }),
        x_thebes_answer={
            'user': {
                'unique_id': 123
            }
        }
    )
    user = client_ticket_list_service.get_user()
    assert user == 10
    assert stub_zenpy.users_args[1]['external_id'] == 123


@patch.object(ClientTicketListService, '_get_zenpy_client', side_effect=Exception('d3eu pau'))
def test_get_user_error(zenpy_users):
    client_ticket_list_service = ClientTicketListService(
        url_path='',
        params=Filter(**{
            "page": 1,
            "page_size": 0
        }),
        x_thebes_answer={
            'user': {
                'unique_id': 123
            }
        }
    )
    with pytest.raises(Exception, match='d3eu pau'):
        user = client_ticket_list_service.get_user()