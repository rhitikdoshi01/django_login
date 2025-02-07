import json
import re
from django.http import JsonResponse

# Email regex pattern
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

def validate_request(request, required_fields, allow_empty_fields=[]):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Invalid JSON format"}, status=400)

    missing_fields = []
    wrong_format_fields = []
    empty_fields = []

    for field, expected_type in required_fields.items():
        if field not in data:
            missing_fields.append(field)
        else:
            value = data[field]

            if not value and field not in allow_empty_fields:
                empty_fields.append(field)

            if field == "email" and not re.match(EMAIL_REGEX, value):
                wrong_format_fields.append(field)

            elif expected_type == int and isinstance(value, str):
                if value.isdigit():  # Convert valid string numbers to int
                    data[field] = int(value)
                else:
                    wrong_format_fields.append(field)

            elif not isinstance(value, expected_type):
                wrong_format_fields.append(field)

    if missing_fields:
        return None, JsonResponse({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)

    if empty_fields:
        return None, JsonResponse({"error": f"Fields cannot be empty: {', '.join(empty_fields)}"}, status=400)

    if wrong_format_fields:
        return None, JsonResponse({"error": f"Invalid format for fields: {', '.join(wrong_format_fields)}"}, status=400)

    return data, None
