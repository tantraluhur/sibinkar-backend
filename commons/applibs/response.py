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

def serializer_error_response(errors) :
    error_message = ""
    for field_name, field_errors in errors.items():
        error_message = f"Invalid data in field {field_name}. {field_errors[0]}"
        break

    return prepare_error_response(error_message)
