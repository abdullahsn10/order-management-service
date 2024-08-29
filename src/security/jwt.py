import jwt
from src import schemas
from src.security.roles import UserRole
from src.settings.settings import JWT_TOKEN_SETTINGS


def verify_token(token: str, credentials_exception) -> schemas.TokenData:
    """
    Verify the token and return the token data if the token is valid
    *Args:
        token: token to be verified
        credentials_exception: exception to be raised if the token is invalid
    *Returns:
        token data if the token is valid
    """
    try:
        payload = jwt.decode(
            token,
            JWT_TOKEN_SETTINGS["PUBLIC_KEY"],
            algorithms=JWT_TOKEN_SETTINGS["ALGORITHM"],
        )

        required_fields = ["sub", "role", "id", "coffee_shop_id", "branch_id"]

        if not all(field in payload for field in required_fields):
            raise credentials_exception

        try:
            role_enum = UserRole(
                payload["role"]
            )  # Convert role string back to UserRole enum
        except ValueError:
            raise credentials_exception

        token_data = schemas.TokenData(
            email=payload["sub"],
            role=role_enum,
            id=payload["id"],
            coffee_shop_id=payload["coffee_shop_id"],
            branch_id=payload["branch_id"],
            token_value=token,
        )
        return token_data
    except jwt.InvalidTokenError:
        raise credentials_exception
