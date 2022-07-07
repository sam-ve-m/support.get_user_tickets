from func.src.domain.validator import TicketFilters
from func.src.services.get_user_tickets import TicketListService
from .stubs import stub_unique_id, stub_ticket_filters

from pytest import fixture


@fixture(scope='function')
def client_ticket_list_service():
    client_ticket_list_service = TicketListService(
        url_path='',
        unique_id=stub_unique_id,
        ticket_filters=stub_ticket_filters
    )
    return client_ticket_list_service  
