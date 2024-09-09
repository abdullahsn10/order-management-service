import grpc
from src.grpc.user_service.protobuf import user_service_pb2, user_service_pb2_grpc
from src.exceptions.exception import OrderServiceException
from src.settings.settings import USER_SERVICE_GRPC_ADDRESS
from src import schemas
from src.definition import GRPC_ERROR_MAPPING


def get_or_create_customer_grpc(
    token: str, request: schemas.CustomerInPOSTOrderRequestBody
) -> schemas.CustomerFullInfo:
    """
    This function is used to send a request to the User Service gRPC server
    to get or create a customer
    *Args:
        token (str): the token of the user
        request (schemas.CustomerInPOSTOrderRequestBody): contains customer details
    *Returns:
        the created/found Customer instance
    """
    try:
        with grpc.insecure_channel(USER_SERVICE_GRPC_ADDRESS) as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            response = stub.GetOrCreateCustomer(
                user_service_pb2.CustomerRequest(
                    token_data=user_service_pb2.TokenData(token=token),
                    customer=user_service_pb2.CustomerPOSTRequestBody(
                        phone_no=request.phone_no, name=request.name
                    ),
                )
            )
            return schemas.CustomerFullInfo(
                id=response.customer.id,
                name=response.customer.name,
                phone_no=response.customer.phone_no,
                coffee_shop_id=response.customer.coffee_shop_id,
                created="2024-09-08 09:59:48.291854",  # Fake date, TODO: Implement this
            )
    except grpc.RpcError as e:
        status_code = (
            GRPC_ERROR_MAPPING.get(e.code()) if e.code() in GRPC_ERROR_MAPPING else 500
        )
        message = e.details() if e.details() else "Internal Server Error"
        raise OrderServiceException(status_code=status_code, message=message)
