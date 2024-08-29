import requests
from typing import Any
from src.exceptions.exception import OrderServiceException


def send_request(
    url: str,
    action: str,
    payload: Any,
    auth_token: str,
):
    """
    This function sends a request to a specific URL with a specific action and payload
    *Args:
        url (str): the URL to send the request to
        action (str): HTTP method (GET, POST, PUT, PATCH, DELETE)
        payload (Any): the payload to send
    *Returns:
        the response from the HTTP request
    """
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }
    try:
        response = requests.request(
            method=action, url=url, headers=headers, json=payload
        )
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        raise OrderServiceException(
            message=http_err.response.json().get("detail"),
            status_code=http_err.response.status_code,
        )
