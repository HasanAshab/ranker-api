from http.client import responses
from rest_framework.renderers import JSONRenderer as DefaultJSONRenderer
from .response import ImmutableResponse


class JSONRenderer(DefaultJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if self._should_modify_data(renderer_context):
            is_successful = self._is_successful_response(renderer_context)
            data = {} if data is None else data

            if isinstance(data, str):
                data = {"message": data}
            elif is_successful:
                data = {self.wrapper_key: data}
            data["success"] = is_successful
            data["message"] = data.get(
                "message",
                self._get_standard_message(renderer_context),
            )
        return super().render(data, accepted_media_type, renderer_context)

    @property
    def wrapper_key(self):
        return "data"

    def _should_modify_data(self, renderer_context=None):
        return renderer_context and not isinstance(
            renderer_context["response"], ImmutableResponse
        )

    def _is_successful_response(self, renderer_context):
        response = renderer_context["response"]
        return 199 < response.status_code < 400

    def _get_standard_message(self, renderer_context):
        response = renderer_context["response"]
        return responses[response.status_code]
