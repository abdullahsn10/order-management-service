from pydantic import BaseModel
from src.security.roles import UserRole


class Token(BaseModel):
    """
    pydantic schema for JWT Token, used in returning a token to the user
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    pydantic schema for the token data
    """

    id: int
    email: str
    role: UserRole
    branch_id: int
    coffee_shop_id: int
    token_value: str = None
