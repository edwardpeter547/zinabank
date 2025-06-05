from django.test import TestCase
from core_apps.common.renderers import GenericJSONRenderer
from rest_framework.response import Response
from rest_framework import status
import json


class MockView:
    object_label = "object"


class GenericJSONRendererTests(TestCase):
    def setUp(self):
        self.renderer = GenericJSONRenderer()
        self.response = Response()

    def test_render_with_data(self):
        """
        Tests that the renderer correctly serializes the response data into JSON format,
        including the HTTP status code and the response data object, and that the rendered
        output matches the expected JSON structure and encoding.
        """
        
        self.response.data = {"name": "Christopher Alexander", "age": 30}
        self.response.status_code = status.HTTP_200_OK

        rendered = self.renderer.render(
            data=self.response.data,
            renderer_context={'response': self.response, 'view': MockView()}
        )
        expected = json.dumps({
            "status": self.response.status_code,
            "object": self.response.data
        }).encode(self.renderer.charset)

        self.assertEqual(
            first=rendered, 
            second=expected, 
            msg="Rendered JSON does not match the expected output."
        )

    def test_render_with_errors(self):
        """
        Tests that the renderer correctly serializes error responses.
        This test sets the response data to contain an "errors" key with a 
        list of error messages and sets the response status code to HTTP 400 (Bad Request). 
        It then renders the response using the custom renderer and asserts that the rendered 
        JSON output matches the expected error data structure.
        """

        self.response.data = {"errors": ["Invalid input"]}
        self.response.status_code = status.HTTP_400_BAD_REQUEST

        rendered = self.renderer.render(
            data=self.response.data,
            renderer_context={'response': self.response, 'view': MockView()}
        )
        
        self.assertEqual(
            json.loads(rendered.decode(self.renderer.charset)), 
            self.response.data,
            msg="Rendered JSON with errors does not match the expected output."
        )

    def test_render_raises_error_when_response_is_missing(self):
        """
        Test that the renderer raises a ValueError when the 'response' 
        key is missing from the renderer_context. This test verifies that 
        attempting to render data without providing a 'response' object in 
        the renderer_context results in a ValueError being raised, with an 
        appropriate error message indicating the missing response.
        """

        data = {"name": "Test User"}
        with self.assertRaises(ValueError) as context:
            self.renderer.render(data=data, renderer_context={'view': MockView()})

        self.assertIn(
            "Response not found in the renderer context.", 
            str(context.exception)
        )

    def test_render_with_custom_object_label(self):
        """
        Tests that the renderer correctly uses a custom object label specified 
        by the view's `object_label` attribute when rendering the response data. 
        Verifies that the rendered JSON output includes the custom label as the key
        and matches the expected structure and encoding.
        """

        self.response.data = {"name": "Test User", "age": 25}
        self.response.status_code = status.HTTP_200_OK

        class CustomView:
            object_label = "custom_object"

        rendered = self.renderer.render(
            data=self.response.data,
            renderer_context={'response': self.response, 'view': CustomView()}
        )
        
        expected = json.dumps({
            "status": self.response.status_code,
            "custom_object": self.response.data
        }).encode(self.renderer.charset)

        self.assertEqual(
            rendered, 
            expected, 
            msg="Rendered JSON with custom object label does not match the expected output."
        )

    def test_render_with_no_data(self):
        """
        Test that the renderer correctly handles responses with no data.
        This test sets the response data to an empty dictionary and the 
        status code to HTTP 204 (No Content). It then renders the response
        and asserts that the output matches the expected JSON structure,
        which should include the status code and an empty object.
        """
        self.response.data = {}
        self.response.status_code = status.HTTP_204_NO_CONTENT

        rendered = self.renderer.render(
            data=self.response.data,
            renderer_context={'response': self.response, 'view': MockView()}
        )
        
        expected = json.dumps({
            "status": self.response.status_code,
            "object": {}
        }).encode(self.renderer.charset)

        self.assertEqual(
            rendered, 
            expected, 
            msg="Rendered JSON with no data does not match the expected output."
        )

    def test_render_with_none_data(self):
        """
        Test that the renderer correctly handles cases where the 
        response data is None. This test sets the response data to None 
        and the status code to HTTP 204 (No Content), then verifies 
        that the renderer outputs a JSON object with the correct status 
        and an empty object.
        """
        self.response.data = None
        self.response.status_code = status.HTTP_204_NO_CONTENT

        rendered = self.renderer.render(
            data=self.response.data,
            renderer_context={'response': self.response, 'view': MockView()}
        )
        
        expected = json.dumps({
            "status": self.response.status_code,
            "object": {}
        }).encode(self.renderer.charset)

        self.assertEqual(
            rendered, 
            expected, 
            msg="Rendered JSON with None data does not match the expected output."
        )
    
