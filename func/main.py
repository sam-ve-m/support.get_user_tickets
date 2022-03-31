from flask import request, Response
import asyncio
import json

from etria_logger import Gladsheim
from heimdall_client.bifrost import Heimdall
from nidavellir import Sindri
from src.service import TicketListService
from src.validator import Filter

event_loop = asyncio.get_event_loop()


def get_user_tickets():
    raw_account_changes_params = request.args
    http_status = 403
    url_path = request.full_path
    x_thebes_answer = request.headers.get("x-thebes-answer")
    heimdall_client = Heimdall()
    try:
        payload = {"status": False}
        is_a_valid_jwt = event_loop.run_until_complete(
            heimdall_client.validate_jwt(jwt=x_thebes_answer)
        )
        if is_a_valid_jwt:
            jwt_content, heimdall_status = event_loop.run_until_complete(
                heimdall_client.decode_payload(jwt=x_thebes_answer)
            )
            filter_params = Filter(**raw_account_changes_params)
            client_account_change_service = TicketListService(
                params=filter_params,
                url_path=url_path,
                x_thebes_answer=jwt_content["decoded_jwt"],
            )
            tickets = client_account_change_service.get_tickets()
            payload.update({"status": True, "tickets": tickets})
            http_status = 200
        response = Response(
            json.dumps(payload, default=Sindri.resolver),
            mimetype="application/json",
            status=http_status,
        )
        return response
    except Exception as e:
        message = "Fission: get_user_tickets"
        Gladsheim.error(e, message)
        response = Response(
            json.dumps({"error": {"message": str(e)}, "status": False}),
            mimetype="application/json",
            status=400,
        )
        return response
