from sqlalchemy.orm import Session
from src import schemas, models
from fastapi import status
from src.utils.api_call import send_request
from src.settings.settings import CUSTOMER_ENDPOINT
from src.grpc.client.user_service_client import grpc_request


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

    # response = send_request(
    #     action="POST",
    #     url=CUSTOMER_ENDPOINT,
    #     payload=request.dict(),
    #     auth_token=auth_token,
    # )
    # customer_instance = schemas.CustomerFullInfo(**response.json())
    # return customer_instance

    # TEST CODE
    # TODO: Remove this code after testing
    response = grpc_request(
        token=auth_token,
        phone_no=request.phone_no,
        name=request.name,
    )
    # dummy date test
    return schemas.CustomerFullInfo(
        id=response.customer.id,
        name=response.customer.name,
        phone_no=response.customer.phone_no,
        coffee_shop_id=response.customer.coffee_shop_id,
        created="2021-10-10T10:10:10",
    )
