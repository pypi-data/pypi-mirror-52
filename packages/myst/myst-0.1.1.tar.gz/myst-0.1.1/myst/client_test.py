import unittest

import mock
import responses
from google.auth.credentials import AnonymousCredentials
from requests import Response
from requests import Session

from myst.client import Client
from myst.exceptions import UnAuthenticatedError


class ClientTest(unittest.TestCase):
    @mock.patch("myst.client.GoogleIDTokenAuth")
    @mock.patch("myst.client.json_response_error_handler_hook")
    def test_client(self, response_error_handler_hook_patch, google_id_token_auth_patch):
        # Test without passing credentials to the client.
        client = Client()

        # Test that both credentials and auth should not be set yet.
        self.assertIsNone(client._credentials)
        self.assertIsNone(client._auth)

        # Test that the session was initialized properly with the expected error handlers.
        self.assertIsInstance(client._session, Session)
        self.assertIsNone(client._session.auth)
        self.assertEqual(client._session.hooks, {"response": [response_error_handler_hook_patch]})

        # Test that trying to access the session through the `session` property before the client is authenticated raises
        # an exception.
        self.assertRaises(UnAuthenticatedError, getattr, client, "session")

        # Test with passing credentials to the client.
        credentials_mock = mock.Mock()

        # Mock out the `GoogleIDTokenAuth` used to apply authorization headers to requests made by the session.
        google_id_token_auth_mock = mock.Mock()
        google_id_token_auth_patch.return_value = google_id_token_auth_mock
        client = Client(credentials=credentials_mock)

        # Test that both credentials and auth were initialized properly, and that the credentials were refreshed
        # to actually fetch the access token from the Google OAuth 2.0 service.
        self.assertEqual(client._credentials, credentials_mock)
        self.assertEqual(client._auth, google_id_token_auth_mock)
        google_id_token_auth_patch.assert_called_once_with(credentials=credentials_mock)

        # Test that the session was initialized properly with the expected error handlers and auth.
        self.assertIsInstance(client._session, Session)
        self.assertEqual(client._session.hooks, {"response": [response_error_handler_hook_patch]})
        self.assertEqual(client._session.auth, google_id_token_auth_mock)

        # Test that we can also now access the session through the `session` property.
        self.assertIsInstance(client.session, Session)

    @mock.patch("myst.client.GoogleIDTokenAuth")
    def test_authenticate(self, google_id_token_auth_patch):
        # Test that we can also authenticate the client asynchronously using `Client.authenticate`.
        client = Client()

        # Test that both credentials and auth should not be set yet.
        self.assertIsNone(client._credentials)
        self.assertIsNone(client._auth)
        self.assertIsInstance(client._session, Session)
        self.assertIsNone(client._session.auth)

        # Mock out the credentials.
        credentials_mock = mock.Mock()

        # Mock out the `GoogleIDTokenAuth` used to apply authorization headers to requests made by the session.
        google_id_token_auth_mock = mock.Mock()
        google_id_token_auth_patch.return_value = google_id_token_auth_mock

        client.authenticate(credentials=credentials_mock)

        # Test that both credentials and auth were initialized properly, and that the credentials were refreshed
        # to actually fetch the access token from the Google OAuth 2.0 service.
        self.assertEqual(client._credentials, credentials_mock)
        self.assertEqual(client._auth, google_id_token_auth_mock)
        google_id_token_auth_patch.assert_called_once_with(credentials=credentials_mock)

        # Test that auth was added to the session.
        self.assertIsInstance(client._session, Session)
        self.assertEqual(client._session.auth, google_id_token_auth_mock)

    @responses.activate
    def test_get(self):
        # Mock response
        responses.add(responses.GET, "https://mock-endpoint.com", json={"message": "Hello!"})

        client = Client(credentials=AnonymousCredentials())
        response = client.get("https://mock-endpoint.com")

        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello!"})
