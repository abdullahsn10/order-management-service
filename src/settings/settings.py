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
SERVICES_COMMUNICATION_SETTINGS = {
    "USER_MANAGEMENT_SERVICE": {
        "URL": os.getenv("USER_MANAGEMENT_SERVICE_URL"),
        "ENDPOINTS": {
            "CUSTOMER": os.getenv("CUSTOMER_ENDPOINT"),
            "USER": os.getenv("USER_ENDPOINT"),
            "COFFEE_SHOP": os.getenv("COFFEE_SHOP_ENDPOINT"),
        },
    },
}
