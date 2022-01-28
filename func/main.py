import logging
import json
from flask import request, Response

from src.validator import Filter
from src.service import ClientTicketListService
from nidavellir.src.uru import Sindri


log = logging.getLogger()


def fn():
    url_path = request.full_path
    raw_account_changes_params = request.json

    try:
        filter_params = Filter(**raw_account_changes_params)
        client_account_change_service = ClientTicketListService(
            params=filter_params, url_path=url_path
        )
        inserted = client_account_change_service.get_tickets()
        return Response(
            json.dumps({"status": inserted}, default=Sindri.default),
            mimetype="application/json",
            status=200,
        )
    except Exception as e:
        log.error(str(e), exc_info=e)
        return Response(
            json.dumps({"error": {"message": str(e)}, "status": False}),
            mimetype="application/json",
            status=400,
        )
