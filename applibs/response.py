from rest_framework.exceptions import ErrorDetail


def prepare_success_response(data=None) -> dict:
    return dict(
        success=True,
        message="Successfully return",
        data=data
    )


def prepare_error_response(message=None) -> dict:
    if hasattr(message, 'items'):
        for key, _ in message.items():
            message[key] = message[key][0]

    return dict(
        success=False,
        message=message if message else "Data Validation Error",
        data=None
    )
