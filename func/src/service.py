# Standards
from typing import Optional, List
import os

# Third part
from decouple import Config, RepositoryEnv, config
from nidavellir import Sindri
from pydantic import BaseModel
from zenpy import Zenpy
from zenpy.lib.api_objects import User, Ticket

# path = os.path.join("/", "app", ".env")
# path = str(path)
# config = Config(RepositoryEnv(path))


class TicketListService:
    zenpy_client = None

    @classmethod
    def _get_zenpy_client(cls):
        if cls.zenpy_client is None:
            cls.zenpy_client = Zenpy(**{
                'email': config('ZENDESK_EMAIL'),
                'password': config('ZENDESK_PASSWORD'),
                'subdomain': config('ZENDESK_SUBDOMAIN')
            })
        return cls.zenpy_client

    def __init__(self, params: BaseModel, url_path: str, x_thebes_answer: dict):
        self.params = params.dict()
        Sindri.dict_to_primitive_types(self.params)
        self.url_path = url_path
        self.x_thebes_answer = x_thebes_answer

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
        return {
            "subject": ticket.subject,
            "id": ticket.id,
            "status": ticket.status,
            "created_at": ticket.created
        }

    def get_user(self) -> User:
        unique_id = self.x_thebes_answer['user']['unique_id']
        zenpy_client = self._get_zenpy_client()
        if user_results := zenpy_client.users(external_id=unique_id):
            user_obj = user_results.values[0]
            return user_obj
        raise Exception('Bad request')
