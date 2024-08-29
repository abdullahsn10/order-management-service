from src import schemas
from src.settings.settings import FIND_USER_ENDPOINT
from src.utils.api_call import send_request


def _find_user(user_id: int, auth_token: str) -> schemas.UserResponse:
    """
    This helper function used to send an API request to User Management Service
    to find a user by id
    *Args:
        user_id (int): the id of the user needed to be found
        auth_token (str): the token of the user
    *Returns:
        the found User instance
    """
    response = send_request(
        action="GET",
        url=FIND_USER_ENDPOINT.format(user_id=user_id),
        payload=None,
        auth_token=auth_token,
    )

    user_instance = schemas.UserResponse(**response.json())
    return user_instance
