import unittest

from requests import Response

from myst.exceptions import MystAPIError
from myst.utils.exception_utils import json_response_error_handler_hook


class MockResponse(Response):
    """Mock response to use in test cases."""

    def __init__(self, status_code, json):
        super(MockResponse, self).__init__()
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


class MockResponseInvalidJson(Response):
    """Mock invalid json response to use in test cases."""

    def __init__(self, status_code):
        super(MockResponseInvalidJson, self).__init__()
        self.status_code = status_code

    def json(self):
        raise ValueError()


class ExceptionUtilsTest(unittest.TestCase):
    def test_response_error_handler_hook(self):
        # Test that the error handler hook just returns the response if the status code is 200.
        response = MockResponse(status_code=200, json={"code": 200, "message": "Success!"})
        self.assertEqual(json_response_error_handler_hook(response), response)

        # Test that the error handler hook raises a `MystAPIError` if the status code is non-200.
        response = MockResponse(status_code=404, json={"code": 404, "message": "Failure."})
        self.assertRaises(MystAPIError, json_response_error_handler_hook, response)

        # Test that the error handler hook raises a `MystAPIError` if we fail to decode json even if the status code is
        # 200.
        response = MockResponseInvalidJson(status_code=200)
        self.assertRaises(MystAPIError, json_response_error_handler_hook, response)
