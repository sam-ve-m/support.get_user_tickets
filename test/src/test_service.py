from unittest.mock import patch
import pytest

from func.src.service import TicketListService
from func.src.validator import Filter

jwt_test = {'user': {'unique_id': 102030}}
params_test = Filter(**{'page': 0, 'page_size': 15})


class StubUser:
    def __init__(self):
        self.id = None
        self.external_id = None

    def set_external_id(self, external_id: int):
        self.external_id = external_id
        return self

    def set_id(self, user_id: int):
        self.id = user_id
        return self


class StubGetUsers:
    def __init__(self):
        self.values = []

    def append_user(self, stub_user: StubUser):
        self.values.append(stub_user)
        return self


class StubTicket:
    def __init__(self):
        self.comment = None
        self.requester = None
        self.id = None
        self.count = 5
        self.subject = 'assunto teste'
        self.status = 'teste'
        self.created = 'data de criação'

    def set_id(self, id):
        self.id = id
        return self

@patch.object(TicketListService, '_get_zenpy_client')
def test_get_user(mock_zenpy_client):
    client_ticket_list_service = TicketListService(url_path='', x_thebes_answer=jwt_test, params=params_test)
    mock_zenpy_client().users.return_value = StubGetUsers().append_user(StubUser())
    user = client_ticket_list_service.get_user()

    assert isinstance(user, StubUser)
    mock_zenpy_client.assert_called()
    mock_zenpy_client().users.asser_called_once_with(external_id=102030)


@patch.object(TicketListService, '_get_zenpy_client')
def test_get_user_raises(mock_zenpy_client):
    client_ticket_list_service = TicketListService(url_path='', x_thebes_answer=jwt_test, params=params_test)
    mock_zenpy_client().users.return_value = None
    with pytest.raises(Exception, match='Bad request'):
        client_ticket_list_service.get_user()


@patch.object(TicketListService, 'get_user', return_value=StubUser().set_id(10))
@patch.object(TicketListService, 'tickets_per_page', return_value=StubTicket())
@patch.object(TicketListService, '_get_zenpy_client')
def test_get_tickets(mock_zenpy_client, mock_tickets_per_page, mock_user):
    client_ticket_list_service = TicketListService(url_path='', x_thebes_answer=jwt_test, params=params_test)
    tickets = client_ticket_list_service.get_tickets()

    assert isinstance(tickets, StubTicket)
    mock_user.assert_called_once()
    mock_zenpy_client().search.assert_called_once_with(type='ticket', requester=10, sort_order='desc', sort_by='created_at')
    mock_tickets_per_page.assert_called_once()

def test_obj_ticket_to_dict():
    client_ticket_list_service = TicketListService(url_path='', x_thebes_answer=jwt_test, params=params_test)
    ticket = StubTicket().set_id(10)
    ticket_dict = client_ticket_list_service.obj_ticket_to_dict(ticket)

    assert type(ticket_dict) is dict
    assert ticket_dict['id'] == 10
    assert ticket_dict['subject'] == 'assunto teste'
    assert ticket_dict['status'] == 'teste'
    assert ticket_dict['created_at'] == 'data de criação'



