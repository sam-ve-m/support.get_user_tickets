# Standards
from typing import Optional, List

# Third part
from pydantic import BaseModel
from zenpy import Zenpy
from zenpy.lib.api_objects import User, Ticket
from decouple import config
from nidavellir.src.uru import Sindri


class ClientTicketListService:
    zenpy_client = Zenpy(**{
        'email': config('ZENDESK_EMAIL'),
        'password': config('ZENDESK_PASSWORD'),
        'subdomain': config('ZENDESK_SUBDOMAIN')
    })

    def __init__(self, params: BaseModel, url_path: str, x_thebes_answer: dict):
        self.params = params.dict()
        Sindri.dict_to_primitive_types(self.params)
        self.url_path = url_path
        self.x_thebes_answer = x_thebes_answer

    def get_tickets(self) -> List[dict]:
        parsed_tickets = []
        if user := self.get_user():
            tickets = self.zenpy_client.search(type='ticket', requester=user.id)
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

    def get_user(self) -> Optional[User]:
        unique_id = self.x_thebes_answer['unique_id']
        if user_results := self.zenpy_client.users(external_id=unique_id):
            user_obj = user_results.values[0]
            return user_obj

# TODO: remove this when teste fission call
if __name__ == "__main__":
    from validator import Filter
    import json
    client_ticket_service = ClientTicketListService(
        params=Filter(
            page=0,
            page_size=15
        ),
        url_path='http://',
        x_thebes_answer={'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491'}
    )
    a = client_ticket_service.get_tickets()
    print(json.dumps({
                "status": True,
                "tickets": a
            }, default=Sindri.resolver))
