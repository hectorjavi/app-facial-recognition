from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def django_validation_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        response_data = {"detail": exc.message}
        response = Response(response_data, status=400)

    return response
