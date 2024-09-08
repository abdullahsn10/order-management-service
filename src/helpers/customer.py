from src import schemas
from src.grpc.user_service.client.user_service_client import get_or_create_customer_grpc


def _get_or_create_customer(
    request: schemas.CustomerInPOSTOrderRequestBody,
    auth_token: str,
) -> schemas.CustomerFullInfo:
    """
    This helper function used to send an gRPC request to User Management Service
    to get or create a customer
    *Args:
        request (schemas.CustomerInPOSTOrderRequestBody): contains customer details
        auth_token (str): the token of the user
    *Returns:
        the created/found Customer instance
    """

    response = get_or_create_customer_grpc(token=auth_token, request=request)
    return response
