import logging
import json
import asyncio
from flask import request, Response

from src.validator import Filter
from src.service import ClientTicketListService
from nidavellir.src.uru import Sindri
from heimdall_client.bifrost import Heimdall


log = logging.getLogger()
event_loop = asyncio.get_event_loop()


def fn():
    url_path = request.full_path
    raw_account_changes_params = request.args
    x_thebes_answer = request.headers.get('x-thebes-answer')
    heimdall_client = Heimdall(logger=log)

    try:
        http_status = 403
        payload = {"status": False}
        is_a_valid_jwt = event_loop.run_until_complete(heimdall_client.validate_jwt(jwt=x_thebes_answer))
        if is_a_valid_jwt:
            jwt_content, heimdall_status = event_loop.run_until_complete(
                heimdall_client.decode_payload(jwt=x_thebes_answer)
            )
            filter_params = Filter(**raw_account_changes_params)
            client_account_change_service = ClientTicketListService(
                params=filter_params, url_path=url_path, x_thebes_answer=jwt_content['decoded_jwt']
            )
            tickets = client_account_change_service.get_tickets()
            payload.update({
                "status": True,
                "tickets": tickets
            })
            http_status = 200
        return Response(
            json.dumps(payload, default=Sindri.resolver),
            mimetype="application/json",
            status=http_status,
        )
    except Exception as e:
        log.error(str(e), exc_info=e)
        return Response(
            json.dumps({"error": {"message": str(e)}, "status": False}),
            mimetype="application/json",
            status=400,
        )
