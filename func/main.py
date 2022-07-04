# Jormungandr
from src.domain.enum import CodeResponse
from src.domain.exceptions import InvalidUniqueId, InvalidJwtToken
from src.domain.validator import Filter
from src.domain.response.model import ResponseModel
from src.services.jwt import JwtService
from src.services.get_user_tickets import TicketListService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request


def get_user_tickets():
    message = "Jormungandr::get_user_tickets"
    raw_account_changes_params = request.args
    url_path = request.full_path
    jwt = request.headers.get("x-thebes-answer")
    try:
        filter_params = Filter(**raw_account_changes_params)
        JwtService.apply_authentication_rules(jwt=jwt)
        decoded_jwt = JwtService.decode_jwt(jwt=jwt)
        client_account_change_service = TicketListService(
            params=filter_params,
            url_path=url_path,
            decoded_jwt=decoded_jwt,
        )
        tickets = client_account_change_service.get_tickets()
        response_model = ResponseModel.build_response(
            result={'Tickets': tickets},
            success=True,
            code=CodeResponse.SUCCESS
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.OK
        )
        return response

    except InvalidUniqueId as ex:
        Gladsheim.error(error=ex, message=f"{message}::'The JWT unique id is not the same user unique id'")
        response_model = ResponseModel.build_response(
            message=ex.msg,
            success=False,
            code=CodeResponse.JWT_INVALID,
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.UNAUTHORIZED
        )
        return response

    except InvalidJwtToken as ex:
        Gladsheim.error(error=ex, message=f"{message}::Invalid JWT token")
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.JWT_INVALID,
            message=ex.msg,
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.UNAUTHORIZED
        )
        return response

    except ValueError as ex:
        Gladsheim.error(ex=ex, message=f'{message}::There are invalid format or extra parameters')
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.INVALID_PARAMS,
            message="There are invalid format or extra/missing parameters",
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.BAD_REQUEST
        )
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=f"{message}::{str(ex)}")
        response_model = ResponseModel.build_response(
            success=False,
            code=CodeResponse.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        )
        response = ResponseModel.build_http_response(
            response_model=response_model,
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
        return response
