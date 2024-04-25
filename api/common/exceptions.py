from rest_framework import status
from rest_framework.views import (
    exception_handler,
)
from rest_framework.exceptions import (
    ValidationError,
)
from rest_framework.response import (
    Response,
)


def validation_exception_handler(exc, context):
    if "non_field_errors" in exc.detail:
        return Response(
            {"message": exc.detail["non_field_errors"][0]},
            status=status.HTTP_400_BAD_REQUEST,
        )
    errors = {}
    for (
        field_name,
        field_errors,
    ) in exc.detail.items():
        errors[field_name] = field_errors[0]
    return Response(
        {"errors": errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


def handler(exc, context):
    if isinstance(exc, ValidationError):
        return validation_exception_handler(exc, context)
    return exception_handler(exc, context)
