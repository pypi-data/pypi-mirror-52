from requests import Session

from myst.exceptions import UnAuthenticatedError
from myst.google_id_token_auth import GoogleIDTokenAuth
from myst.utils.core_utils import get_user_agent
from myst.utils.exception_utils import json_response_error_handler_hook


class Client(object):
    """HTTP client for interacting with the Myst API."""

    def __init__(self, credentials=None):
        self._credentials = credentials
        self._auth = None

        # Initialize the `requests` session.
        self._session = Session()

        # Add error handling and custom headers.
        self._session.hooks["response"].extend([json_response_error_handler_hook])
        self._session.headers.update({"User-Agent": get_user_agent()})

        # If credentials were provided, initialize authorization and authorize session.
        if self._credentials is not None:
            self.authenticate(credentials=self._credentials)

    @property
    def session(self):
        """The `requests` session to use to make authenticated requests to the Myst API.

        Returns:
            session (requests.Session): session to make authenticated requests to the Myst API with

        Raises:
            ValueError: You need to authenticate first before using the session.
        """
        if self._auth is None:
            raise UnAuthenticatedError("You need to authenticate first using `myst.authenticate(...)`.")
        return self._session

    def authenticate(self, credentials):
        """Authenticates this client using the given credentials.

        Note that this also adds the appropriate `Authorization` header to the session.

        Args:
            credentials (google.oauth2.credentials.Credentials, google.oauth2.service_account.IDTokenCredentials, or
                google.auth.credentials.AnonymousCredentials): user or service account credentials to authenticate the
                    client using
        """
        self._credentials = credentials
        self._auth = GoogleIDTokenAuth(credentials=credentials)
        self._auth.refresh()
        self._session.auth = self._auth

    def get(self, url):
        """Makes an authorized HTTP 'GET` request to the given Myst API endpoint.

        Args:
            url (str): Myst API endpoint to make request to

        Returns:
            response (requests.Response): response
        """
        response = self.session.get(url)
        return response
