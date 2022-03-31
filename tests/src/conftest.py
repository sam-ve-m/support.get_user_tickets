from func.src.validator import Filter
from func.src.service import TicketListService

from pytest import fixture

jwt_test = {'user': {'unique_id': 102030}}
params_test = Filter(**{'page': 0, 'page_size': 15})


@fixture(scope='function')
def client_ticket_list_service():
    client_ticket_list_service = TicketListService(
        url_path='', x_thebes_answer=jwt_test, params=params_test
    )
    return client_ticket_list_service  
