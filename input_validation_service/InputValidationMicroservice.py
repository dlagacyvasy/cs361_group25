"""
Input Validation Microservice
------------------------------

This microservice validates and normalizes user input.
It communicates using JSON over standard input and output (stdin/stdout).

It is designed to be reusable and independent from any specific application.
"""

import sys
import json


def validate_selection(input_value, allowed_values, normalize=True):
    """
    Validates selection-based input.
    Accepts either:
    - A number corresponding to the index (1-based)
    - A string matching one of the allowed values (case-insensitive)
    """

    # Handle numeric selection (e.g., "1", "2")
    if input_value.isdigit():
        index = int(input_value)
        if 1 <= index <= len(allowed_values):
            return True, allowed_values[index - 1]

    # Handle text selection
    for value in allowed_values:
        if input_value.lower() == value.lower():
            return True, value if normalize else input_value

    return False, None


def validate_text(input_value):
    """
    Validates generic text input (non-empty string).
    """
    if isinstance(input_value, str) and input_value.strip() != "":
        return True, input_value.strip()

    return False, None


def process_request(request):
    """
    Processes incoming validation request.
    """

    input_value = request.get("input_value")
    allowed_values = request.get("allowed_values", [])
    input_type = request.get("input_type")
    normalize = request.get("normalize", True)

    if input_type == "selection":
        is_valid, normalized_value = validate_selection(
            input_value, allowed_values, normalize
        )

    elif input_type == "text":
        is_valid, normalized_value = validate_text(input_value)

    else:
        return {
            "is_valid": False,
            "normalized_value": None,
            "message": "Unsupported input type."
        }

    if is_valid:
        return {
            "is_valid": True,
            "normalized_value": normalized_value,
            "message": "Input is valid."
        }
    else:
        return {
            "is_valid": False,
            "normalized_value": None,
            "message": "Invalid input."
        }


def main():
    """
    Reads JSON request from stdin and writes JSON response to stdout.
    """

    try:
        raw_input = sys.stdin.read()
        request = json.loads(raw_input)

        response = process_request(request)

    except Exception as e:
        response = {
            "is_valid": False,
            "normalized_value": None,
            "message": f"Error processing request: {str(e)}"
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
