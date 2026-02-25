from django.utils.translation import gettext as _
from rest_framework.views import exception_handler


def unified_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    message = _("Request failed.")
    details = response.data
    if isinstance(response.data, dict):
        message = response.data.get("detail") or message
    response.data = {
        "error": {
            "code": str(response.status_code),
            "message": str(message),
            "details": details,
        }
    }
    return response
