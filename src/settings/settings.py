import os
from dotenv import load_dotenv


# load environment variables
load_dotenv()

# load database settings
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_SERVICE = os.getenv("DB_SERVICE")
POSTGRES_DB = os.getenv("POSTGRES_DB")


# database url
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_SERVICE}/{POSTGRES_DB}"
)

# database settings
DATABASE_SETTINGS = {
    "URL": SQLALCHEMY_DATABASE_URL,
}


# security settings
PUBLIC_KEY = os.getenv("PUBLIC_KEY")


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
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
ORDER_NOTIFICATION_QUEUE = os.getenv("ORDER_NOTIFICATION_QUEUE")

# Redis and Cache settings
REDIS = {
    "HOST": os.getenv("REDIS_HOST"),
    "PORT": os.getenv("REDIS_PORT"),
    "DB": os.getenv("REDIS_DB"),
    "PASSWORD": os.getenv("REDIS_PASSWORD"),
}

ORDERS_CACHE_KEY = "orders:{coffee_shop_id}:{status}:{page}:{size}"
ORDERS_CACHE_EXPIRATION = 300  # 5 minutes

# gRPC settings
USER_SERVICE_GRPC_HOST = os.getenv("GRPC_HOST")
USER_SERVICE_GRPC_PORT = os.getenv("GRPC_PORT")
USER_SERVICE_GRPC_ADDRESS = f"{USER_SERVICE_GRPC_HOST}:{USER_SERVICE_GRPC_PORT}"


# docs settings
OPENAPI_URL = os.getenv("OPENAPI_URL")
ROOT_PATH = os.getenv("ROOT_PATH")
