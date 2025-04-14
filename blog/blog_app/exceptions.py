from rest_framework.views import exception_handler
from rest_framework.response import Response
from .custom_exceptions import EmailSendingError


def custom_exception_handler(exc, context):
    # Call the default DRF exception handler first
    response = exception_handler(exc, context)

    # Check if it's an instance of your custom exception
    if isinstance(exc, EmailSendingError):
        response.data["error"] = exc.message
        response.data["recipient"] = exc.recipient
        response.status_code = (
            exc.status_code
        )  # You can change the status code if needed

    return response
