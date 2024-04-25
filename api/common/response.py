from rest_framework.response import Response


class ImmutableResponse(Response):
    """
    This Response will not be modefied
    by the Renderer. It will be rendered
    as it is.
    """

    pass
