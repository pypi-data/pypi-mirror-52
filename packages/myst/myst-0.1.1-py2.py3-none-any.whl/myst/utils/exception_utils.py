"""This module contains various utility functions related to exceptions."""
from six.moves import http_client

from myst.exceptions import MystAPIError


def json_response_error_handler_hook(response, *args, **kwargs):
    """Simple `requests` error handler hook that checks for any Myst API errors or json decode errors and raises
    corresponding native Python errors.

    Args:
        response (requests.Response): response
        *args: unused, additional arguments
        **kwargs: unused, additional keyword arguments

    Returns:
        response (requests.Response): response
    """
    try:
        response_json = response.json()
    except ValueError:
        raise MystAPIError(
            http_status_code=response.status_code,
            code=response.status_code,
            message="Failed to decode json from response. Contents of response:\n'{content}'".format(
                content=response.content
            ),
        )
    if response.status_code != http_client.OK:
        raise MystAPIError(
            http_status_code=response.status_code, code=response_json.get("code"), message=response_json.get("message")
        )
    return response
