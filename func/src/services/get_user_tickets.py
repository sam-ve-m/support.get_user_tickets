# Jormungandr
from func.src.domain.exceptions import InvalidUniqueId

# Standards
from typing import List

# Third party
from etria_logger import Gladsheim
from decouple import config
from nidavellir import Sindri
from pydantic import BaseModel
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

    def __init__(self, params: BaseModel, url_path: str, decoded_jwt: dict):
        self.params = params.dict()
        self.url_path = url_path
        self.decoded_jwt = decoded_jwt
        Sindri.dict_to_primitive_types(self.params)

    def get_user(self) -> User:
        unique_id = self.decoded_jwt["user"]["unique_id"]
        zenpy_client = self._get_zenpy_client()
        user_result = zenpy_client.users(external_id=unique_id)
        if user_result:
            user_zenpy = user_result.values[0]
            return user_zenpy
        message = (
            f"get_user::There is no user with this unique id specified"
            f"::{self.decoded_jwt['user']['unique_id']}"
        )
        Gladsheim.error(message=message)
        raise InvalidUniqueId

    def get_tickets(self) -> List[dict]:
        user = self.get_user()
        zenpy_client = self._get_zenpy_client()
        tickets = zenpy_client.search(type='ticket', requester=user.id, sort_order='desc', sort_by='created_at')
        parsed_tickets = self.tickets_per_page(tickets)
        return parsed_tickets

    def tickets_per_page(self, tickets: Ticket):
        parsed_tickets = []
        start = self.params["page"] * self.params["page_size"]
        if start < tickets.count:
            end = start + self.params["page_size"]
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
