from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from core_apps.user_auth.middleware import CustomHeaderMiddleware


class CustomHeaderMiddlewareTest(TestCase):
    """
    Unit tests for the CustomHeaderMiddleware.

    This middleware is responsible for injecting the authenticated user's email
    into the response header as 'X-Django-User'. These tests verify that:

    - Authenticated users receive the correct header in the response.
    - Non authenticated users e.g. Anonymous users do not receive the header.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = lambda request: self._get_fake_response()
        self.middleware = CustomHeaderMiddleware(self.get_response)
    
    def _get_fake_response(self):
        """
        Returns a simple HTTP 200 OK response used to simulate the
        final response in the middleware chain.
        """
        from django.http import HttpResponse
        return HttpResponse("OK")
    
    def _get_user(self):
        """Creates and returns a test user with necessary attributes."""

        User = get_user_model()
        return User.objects.create_user(
            email="test@example.com",
            first_name="Firstname",
            last_name="Lastname",
            id_no="22338837",
            security_question="birth_city",
            security_answer="Omuma",
            password="welcome"
        )
    
    def test_authenticated_user_gets_custom_header(self):
        """
        Test that an authenticated user's email is correctly added
        to the response headers by the middleware.

        The middleware should check if the user is authenticated and,
        if so, add 'X-Django-User' to the response with the user's email.
        """

        # create and add the user to the request
        user = self._get_user()
        request = self.factory.get("/")
        request.user = user

        # pass on the request to the middleware
        response = self.middleware(request)

        # check if the expected header info is added to the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Django-User", response)
        self.assertEqual(response["X-Django-User"], user.email)

    def test_anonymous_user_has_no_custom_header(self):
        """
        Test that for non authenticated user custom header X-Django-User
        is not added to the response headers by the middleware.
        """
         
        anonymous_user = AnonymousUser()
        request = self.factory.get("/")
        request.user = anonymous_user

        # pass on the request to the middleware
        response = self.middleware(request)

        # check if the expected header info is added to the response
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("X-Django-User", response)
