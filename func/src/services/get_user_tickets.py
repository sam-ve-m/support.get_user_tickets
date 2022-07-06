# Jormungandr
from ..domain.exceptions import InvalidUniqueId

# Third party
from etria_logger import Gladsheim
from decouple import config
from zenpy import Zenpy
from zenpy.lib.api_objects import User, Ticket


class TicketListService:
    zenpy_client = None

    @classmethod
    def _get_zenpy_client(cls):
        if cls.zenpy_client is None:
            try:
                cls.zenpy_client = Zenpy(
                    **{
                        "email": config("ZENDESK_EMAIL"),
                        "password": config("ZENDESK_PASSWORD"),
                        "subdomain": config("ZENDESK_SUBDOMAIN"),
                    }
                )
            except Exception as ex:
                message = "_get_zenpy_client::error to get Zenpy Client"
                Gladsheim.error(error=ex, message=message)
                raise ex
        return cls.zenpy_client

    def __init__(self, ticket_filters: dict, url_path: str, unique_id: str):
        self.ticket_filters = ticket_filters
        self.url_path = url_path
        self.unique_id = unique_id

    def get_user(self) -> User:

        zenpy_client = self._get_zenpy_client()
        user_result = zenpy_client.users(external_id=self.unique_id)
        if user_result:
            user_zenpy = user_result.values[0]
            return user_zenpy
        message = (
            f"get_user::There is no user with this unique id specified"
            f"::{self.unique_id}"
        )
        Gladsheim.info(message=message)
        raise InvalidUniqueId

    def get_tickets(self) -> dict:
        user = self.get_user()
        zenpy_client = self._get_zenpy_client()
        tickets = zenpy_client.search(type='ticket', requester=user.id, sort_order='desc', sort_by='created_at')
        parsed_tickets = self.tickets_per_page(tickets)
        result = {
            "tickets": parsed_tickets
        }
        return result

    def tickets_per_page(self, tickets: Ticket):
        parsed_tickets = []
        start = self.ticket_filters["page"] * self.ticket_filters["page_size"]
        if start < tickets.count:
            end = start + self.ticket_filters["page_size"]
            end = end if end <= tickets.count else tickets.count
            for ticket in tickets[start:end]:
                parsed_tickets.append(self.obj_ticket_to_dict(ticket))
        return parsed_tickets

    @staticmethod
    def obj_ticket_to_dict(ticket: Ticket) -> dict:
        ticket = {
            "subject": ticket.subject,
            "id": ticket.id,
            "status": ticket.status,
            "created_at": ticket.created
        }
        return ticket
