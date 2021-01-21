"""Module for broad, generic utility functions."""

import re


def camel_to_snake(input_text):
    """Converts the input text from camel case to snake case."""
    input_text = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', input_text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', input_text).lower()
