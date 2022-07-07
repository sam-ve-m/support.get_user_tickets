# Jormungandr
from tests.src.stubs import StubUser, StubTicket, StubGetUsers
from func.src.services.get_user_tickets import TicketListService
from func.src.domain.exceptions import InvalidUniqueId

# Standards
from unittest.mock import patch

# Third party
import pytest


@patch.object(TicketListService, '_get_zenpy_client')
def test_get_user(mock_zenpy_client, client_ticket_list_service):
    mock_zenpy_client().users.return_value = StubGetUsers().append_user(StubUser(external_id='102030'))
    user = client_ticket_list_service.get_user()

    assert isinstance(user, StubUser)
    assert user.external_id == client_ticket_list_service.unique_id


@patch.object(TicketListService, '_get_zenpy_client')
def test_get_user_if_zenpy_client_was_called(mock_zenpy_client, client_ticket_list_service):
    client_ticket_list_service.get_user()

    mock_zenpy_client.assert_called_once_with()


@patch.object(TicketListService, '_get_zenpy_client')
def test_get_user_if_zenpy_client_users_was_called(mock_zenpy_client, client_ticket_list_service):
    client_ticket_list_service.get_user()

    mock_zenpy_client().users.assert_called_once_with(external_id='102030')


@patch.object(TicketListService, '_get_zenpy_client')
def test_get_user_raises(mock_zenpy_client, client_ticket_list_service):
    mock_zenpy_client().users.return_value = None
    with pytest.raises(InvalidUniqueId):
        client_ticket_list_service.get_user()


@patch.object(TicketListService, 'get_user', return_value=StubUser(id=10))
@patch.object(TicketListService, 'tickets_per_page', return_value=[StubTicket()])
@patch.object(TicketListService, '_get_zenpy_client')
def test_get_tickets(mock_zenpy_client, mock_tickets_per_page, mock_get_user, client_ticket_list_service):
    result = client_ticket_list_service.get_tickets()

    assert isinstance(result, dict)
    assert isinstance(result.get("tickets")[0], StubTicket)


@patch.object(TicketListService, 'get_user')
@patch.object(TicketListService, 'tickets_per_page')
@patch.object(TicketListService, '_get_zenpy_client')
def test_get_tickets_if_get_user_was_called(mock_zenpy_client, mock_tickets_per_page, mock_get_user, client_ticket_list_service):
    client_ticket_list_service.get_tickets()

    mock_get_user.assert_called_once_with()


@patch.object(TicketListService, 'get_user')
@patch.object(TicketListService, 'tickets_per_page')
@patch.object(TicketListService, '_get_zenpy_client')
def test_get_tickets_if_zenpy_client_was_called(mock_zenpy_client, mock_tickets_per_page, mock_get_user, client_ticket_list_service):
    client_ticket_list_service.get_tickets()

    mock_zenpy_client.assert_called_once_with()


@patch.object(TicketListService, 'get_user', return_value=StubUser(id=10))
@patch.object(TicketListService, 'tickets_per_page')
@patch.object(TicketListService, '_get_zenpy_client')
def test_get_tickets_if_zenpy_client_search_was_called(mock_zenpy_client, mock_tickets_per_page, mock_get_user, client_ticket_list_service):
    client_ticket_list_service.get_tickets()

    mock_zenpy_client().search.assert_called_once_with(type='ticket', requester=10, sort_order='desc', sort_by='created_at')


@patch.object(TicketListService, 'get_user')
@patch.object(TicketListService, 'tickets_per_page', return_value=StubTicket())
@patch.object(TicketListService, '_get_zenpy_client')
def test_get_tickets_if_tickets_per_page_was_called(mock_zenpy_client, mock_tickets_per_page, mock_get_user, client_ticket_list_service):
    client_ticket_list_service.get_tickets()

    mock_tickets_per_page.assert_called_once_with(mock_zenpy_client().search())


def test_obj_ticket_to_dict(client_ticket_list_service):
    ticket_dict = client_ticket_list_service.obj_ticket_to_dict(StubTicket(id=10))

    assert isinstance(ticket_dict, dict)
    assert ticket_dict['id'] == 10
    assert ticket_dict['subject'] == 'assunto teste'
    assert ticket_dict['status'] == 'teste'
    assert ticket_dict['created_at'] == 'data de criação'
