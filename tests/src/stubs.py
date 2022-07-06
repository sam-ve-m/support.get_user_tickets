from func.src.domain.validator import TicketFilters


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


stub_unique_id = "102030"
stub_ticket_filters = TicketFilters(**{'page': 0, 'page_size': 15}).dict()
