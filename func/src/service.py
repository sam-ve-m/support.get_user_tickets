# Standards
import datetime

# Third part
from pydantic import BaseModel
from zenpy import Zenpy
from decouple import config


class ClientTicketListService:
    def __init__(self, params: BaseModel, url_path: str):
        self.params = params.dict()
        self.url_path = url_path
        self.credentials = {
            'email': config('ZENDESK_EMAIL'),
            'password': config('ZENDESK_PASSWORD'),
            'subdomain': config('ZENDESK_SUBDOMAIN')
        }

    def get_tickets(self):
        zenpy_client = Zenpy(**self.credentials)
        a = []
        for ticket in zenpy_client.users():
            a.append(str(ticket))
        return {"a": a}
