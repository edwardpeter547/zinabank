import unittest
from unittest.mock import patch, MagicMock
from django.test import (
    TestCase, 
    RequestFactory, 
    override_settings,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from core_apps.common.cookie_auth import CookieAuthentication


class CookieAuthenticationTestCase(TestCase):
    def setUp(self):
        """
        Set up test dependencies for cookie-based authentication tests.

        Initializes:
            self.auth: An instance of CookieAuthentication for testing authentication logic.
            self.factory: A RequestFactory instance for creating mock requests.
            self.valid_token: A valid JWT access token string for authentication tests.
        """
        self.auth = CookieAuthentication()
        self.factory = RequestFactory()
        self.valid_token = str(AccessToken())

    @patch.object(CookieAuthentication, 'get_validated_token')
    @patch.object(CookieAuthentication, 'get_user')
    def test_authenticate_with_authorization_header(self, mock_get_user, mock_get_validated_token):
        """
        Test that the authentication method correctly retrieves the user and token
        when a valid 'Authorization' header with a Bearer token is present in the request.

        Mocks:
            - mock_get_user: Simulates retrieval of a user object.
            - mock_get_validated_token: Simulates validation and retrieval of a token.

        Asserts:
            - The returned user matches the mocked user.
            - The returned token matches the valid token.
        """
        mock_get_user.return_value = 'testuser'
        mock_get_validated_token.return_value = self.valid_token

        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f"Bearer {self.valid_token}"
        user, token = self.auth.authenticate(request)

        self.assertEqual(user, 'testuser')
        self.assertEqual(token, self.valid_token)

    
    @patch.object(CookieAuthentication, 'get_validated_token')
    @patch.object(CookieAuthentication, 'get_user')
    def test_authenticate_with_cookie(self, mock_get_user, mock_get_validated_token):
        """
        Tests the `CookieAuthentication.authenticate` method to ensure that a user 
        is correctly authenticated when a valid token is present in the request 
        cookies. Mocks the user retrieval and token validation methods, sets a 
        test_cookie, and asserts that the returned user and token match the 
        expected values.
        """
        mock_get_user.return_value = 'testuser'
        mock_get_validated_token.return_value = self.valid_token

        with override_settings(COOKIE_NAME='test_cookie'):
            auth = CookieAuthentication()
            request = self.factory.get('/')
            request.COOKIES['test_cookie'] = self.valid_token

            user, token = auth.authenticate(request)

            self.assertEqual(user, 'testuser')
            self.assertEqual(token, self.valid_token)

    def test_authenticate_without_token(self):
        """
        Test that the authenticate method returns None when no 
        authentication token is present in the request.
        """
        request = self.factory.get('/')
        result = self.auth.authenticate(request)
        self.assertIsNone(result)

    @override_settings(COOKIE_NAME='test_cookie')
    @patch.object(
        CookieAuthentication, 
        'get_validated_token', 
        side_effect=TokenError("Token expired")
    )
    def test_authenticate_with_invalid_token_logs_error(self, mock_get_validated_token):
        """
        Test that the authenticate method logs an error and returns None when an invalid 
        (expired) token is provided.

        This test:
        - Overrides the COOKIE_NAME setting to 'test_cookie'.
        - Mocks the get_validated_token method of CookieAuthentication to raise a 
          TokenError with the message "Token expired".
        - Patches the logger's error method to track error logging.
        - Simulates a request with an invalid token in the cookie.
        - Asserts that authenticate returns None.
        - Asserts that an error is logged exactly once with the expected error message.
        """
        with patch('core_apps.common.cookie_auth.logger.error') as mock_logger:
            request = self.factory.get('/')
            request.COOKIES['test_cookie'] = self.valid_token

            result = self.auth.authenticate(request)
            self.assertIsNone(result)
            mock_logger.assert_called_once()
            self.assertIn("Token validation error: Token expired", mock_logger.call_args[0][0])

    @patch.object(CookieAuthentication, 'get_header')
    def test_authenticate_when_there_are_no_headers_on_request(self, mock_get_header):
        """
        Test that the authenticate method returns None when there are no authentication 
        headers present in the request. This test mocks the header retrieval to return 
        None, simulates a GET request, and verifies that:
        - The header retrieval method is called once with the request.
        - The authenticate method returns None, indicating no authentication occurred 
        due to missing headers.
        """
        mock_get_header.return_value = None
        request = self.factory.get('/')
        result = self.auth.authenticate(request)
        mock_get_header.assert_called_once_with(request)
        self.assertIsNone(result, msg="Expected None when no headers are present")

    @patch.object(CookieAuthentication, 'get_header')
    def test_get_raw_token_is_called_when_headers_are_present(self, mock_get_header):
        """
        Test that the `get_raw_token` method is called with the correct header value when 
        headers are present. This test patches the `get_header`, `get_raw_token`, 
        `get_validated_token`, and `get_user` methods of the`CookieAuthentication` class. 
        It simulates a request with an `Authorization` header, ensures that`get_header` 
        returns the header value, and verifies that `get_raw_token` and `get_user` are called 
        with the expected arguments.
        """
        with patch.object(CookieAuthentication, 'get_raw_token') as mock_get_raw_token, \
            patch.object(CookieAuthentication, 'get_validated_token') as mock_get_validated_token, \
            patch.object(CookieAuthentication, 'get_user') as mock_get_user:

            access_token = AccessToken()
            mock_get_validated_token.return_value = access_token
            mock_get_user.return_value = 'testuser'
            mock_get_raw_token.return_value = access_token

            request = self.factory.get('/')
            request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"

            # Simulate get_header() returning the header value
            mock_get_header.return_value = request.META['HTTP_AUTHORIZATION']

            self.auth.authenticate(request)
            mock_get_raw_token.assert_called_once_with(request.META['HTTP_AUTHORIZATION'])
            mock_get_user.assert_called_once_with(access_token)

