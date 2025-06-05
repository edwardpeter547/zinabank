import json
from typing import Any, Optional, Union
from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class GenericJSONRenderer(JSONRenderer):
    """
    Custom JSON renderer that formats the response data with a 'data' key.
    """
    charset = 'utf-8'
    object_label = 'object'

    def render(self, data: Any, accepted_media_type: Optional[str] = None, renderer_context: dict = None) -> Union[bytes, str]:
        """
        Renders the given data into JSON, wrapping it with a status code and a customizable object label.

        Args:
            data (Any): The response data to render.
            accepted_media_type (Optional[str]): The accepted media type.
            renderer_context (dict, optional): Context dictionary containing view and response objects.

        Returns:
            Union[bytes, str]: The rendered JSON response as bytes.

        Raises:
            ValueError: If the response object is not found in the renderer context.
        """
        if renderer_context is None:
            renderer_context = {}

        view = renderer_context.get('view', None)
        if hasattr(view, 'object_label'):
            object_label = view.object_label
        else:
            object_label = self.object_label
        
        response: Response = renderer_context.get('response', None)
        if not response:
            raise ValueError(_("Response not found in the renderer context."))
        
        status_code = response.status_code

        if data is None:    
            data = {}
        errors = data.get('errors', None)

        if errors is not None:
            return super(GenericJSONRenderer, self).render(data)
        
        return json.dumps({
            "status": status_code,
            object_label: data
        }).encode(self.charset)
        
