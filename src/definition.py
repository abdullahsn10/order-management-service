# UserRole to OrderStatus Mapping
import grpc

ROLE_STATUS_MAPPING = {
    "CASHIER": ["CLOSED"],
    "CHEF": ["IN_PROGRESS", "COMPLETED"],
}


# gRPC error mapping
GRPC_ERROR_MAPPING = {
    grpc.StatusCode.UNAUTHENTICATED: 401,
    grpc.StatusCode.PERMISSION_DENIED: 403,
    grpc.StatusCode.NOT_FOUND: 404,
    grpc.StatusCode.ALREADY_EXISTS: 409,
    grpc.StatusCode.INVALID_ARGUMENT: 400,
    grpc.StatusCode.INTERNAL: 500,
    grpc.StatusCode.UNIMPLEMENTED: 501,
    grpc.StatusCode.UNKNOWN: 500,
}
