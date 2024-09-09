import os
from dotenv import load_dotenv


# load environment variables
load_dotenv()

# database settings
DATABASE_SETTINGS = {
    "URL": os.getenv("SQLALCHEMY_DATABASE_URL"),
}

# security settings
with open(os.getenv("PUBLIC_KEY_PATH"), "r") as key_file:
    PUBLIC_KEY = key_file.read()


JWT_TOKEN_SETTINGS = {
    "PUBLIC_KEY": PUBLIC_KEY,
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
}

# Services Communication settings
USER_SERVICE_BASE_URL = os.getenv("USER_SERVICE_BASE_URL")


# USER SERVICE ENDPOINTS
CUSTOMER_ENDPOINT = USER_SERVICE_BASE_URL + "/customers"
USER_ENDPOINT = USER_SERVICE_BASE_URL + "/users"
FIND_USER_ENDPOINT = USER_ENDPOINT + "/{user_id}"
COFFEE_SHOP_ENDPOINT = USER_SERVICE_BASE_URL + "/coffee-shops"

# RabbitMQ and Notification Service settings
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
ORDER_NOTIFICATION_QUEUE = os.getenv("ORDER_NOTIFICATION_QUEUE")

# Redis and Cache settings
REDIS = {
    "HOST": os.getenv("REDIS_HOST"),
    "PORT": os.getenv("REDIS_PORT"),
    "DB": os.getenv("REDIS_DB"),
}

ORDERS_CACHE_KEY = "orders:{coffee_shop_id}:{status}:{page}:{size}"
ORDERS_CACHE_EXPIRATION = 300  # 5 minutes

# gRPC settings
USER_SERVICE_GRPC_HOST = os.getenv("USER_SERVICE_GRPC_HOST")
USER_SERVICE_GRPC_PORT = os.getenv("USER_SERVICE_GRPC_PORT")
USER_SERVICE_GRPC_ADDRESS = f"{USER_SERVICE_GRPC_HOST}:{USER_SERVICE_GRPC_PORT}"
