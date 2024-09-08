import grpc
from src.grpc.protobuf import user_service_pb2, user_service_pb2_grpc


def grpc_request(token: str, phone_no: str, name: str):
    """
    This function is used to send a request to the User Service gRPC server
    to get or create a customer
    *Args:
        token (str): the token of the user
        phone_no (str): phone number of the customer
        name (str): name of the customer
    *Returns:
        the created/found Customer instance
    """
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        response = stub.GetOrCreateCustomer(
            user_service_pb2.CustomerRequest(
                token_data=user_service_pb2.TokenData(token=token),
                customer=user_service_pb2.CustomerPOSTRequestBody(
                    phone_no=phone_no, name=name
                ),
            )
        )
        return response
