from func.src.validator import Filter
from func.src.service import TicketListService

from pytest import fixture


jwt_test = {'user': {'unique_id': 102030}}
params_test = Filter(**{'page': 0, 'page_size': 15})


class StubUser:
    def __init__(self, id=None, external_id=None):
        self.id = id or None
        self.external_id = external_id or None


class StubGetUsers:
    def __init__(self, values=None):
        self.values = values or []

    def append_user(self, stub_user: StubUser):
        self.values.append(stub_user)
        return self


class StubTicket:
    def __init__(self, comment=None, requester=None, id=None, count=None, subject=None, status=None, created=None):
        self.comment = comment or None
        self.requester = requester or None
        self.id = id or None
        self.count = count or 5
        self.subject = subject or 'assunto teste'
        self.status = status or 'teste'
        self.created = created or 'data de criação'


@fixture(scope='function')
def client_ticket_list_service():
    client_ticket_list_service = TicketListService(
        url_path='', x_thebes_answer=jwt_test, params=params_test
    )
    return client_ticket_list_service
