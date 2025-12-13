from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status as drf_status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(exc.message_dict if hasattr(exc, "message_dict") else exc.messages)

    response = exception_handler(exc, context)

    if response is not None:
        data = response.data

        if isinstance(exc, DRFValidationError):
            normalized = {"errors": data}
            response.data = normalized
            return response

        if isinstance(data, dict) and "detail" in data:
            response.data = {
                "detail": data["detail"],
            }
            return response
        return response
    return Response(
        {
            "detail": "Internal server error. Please contact support if the problem persists",
        },
        status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
