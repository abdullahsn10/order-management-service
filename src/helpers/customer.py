from sqlalchemy.orm import Session
from src import schemas, models
from fastapi import status
from src.utils.api_call import send_request
from src.settings.settings import SERVICES_COMMUNICATION_SETTINGS


def _get_or_create_customer(
    request: schemas.CustomerInPOSTOrderRequestBody,
    auth_token: str,
) -> schemas.CustomerFullInfo:
    """
    This helper function used to send an API request to User Management Service
    to get or create a customer
    *Args:
        request (schemas.CustomerInPOSTOrderRequestBody): contains customer details
        auth_token (str): the token of the user
    *Returns:
        the created/found Customer instance
    """
    endpoint_url = (
        f"{SERVICES_COMMUNICATION_SETTINGS['USER_MANAGEMENT_SERVICE']['URL']}"
        f"{SERVICES_COMMUNICATION_SETTINGS['USER_MANAGEMENT_SERVICE']['ENDPOINTS']['CUSTOMER']}"
    )
    response = send_request(
        action="POST",
        url=endpoint_url,
        payload=request.dict(),
        auth_token=auth_token,
    )
    customer_instance = schemas.CustomerFullInfo(**response.json())
    return customer_instance
