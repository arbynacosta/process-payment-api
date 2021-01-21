"""Module for the payment request model."""

from datetime import datetime
import json as jsonlib

from dateutil.parser import parse as dtparse

from app.utils.generic_utils import camel_to_snake


class Payment():
    """Payment model to be used within the API code."""
    # pylint: disable=too-many-instance-attributes

    def __init__(self,
                 amount: int,
                 card_holder: str,
                 credit_card_number: str,
                 expiration_date: datetime,
                 security_code=None):

        self.amount = amount
        self.credit_card_number = credit_card_number
        self.expiration_date = expiration_date
        self.security_code = security_code

        # Properties without validation functions
        self.card_holder = card_holder

    @classmethod
    def from_json(cls, input_json):
        """Parses the request JSON into a `Payment` instance."""
        return cls.from_dict(jsonlib.loads(input_json))

    @classmethod
    def from_dict(cls, input_dict):
        """Parses the request dictionary into a `Payment` instance."""
        snake_case_dict = {camel_to_snake(k): v for k, v in input_dict.items()}
        return cls(**snake_case_dict)

    @property
    def amount(self):  # pylint: disable=missing-function-docstring
        return self._amount

    @amount.setter
    def amount(self, value):
        if not value or int(value) <= 0:
            raise ValueError(f"Invalid amount: {value}")
        self._amount = int(value)

    @property
    def credit_card_number(self):  # pylint: disable=missing-function-docstring
        return self._credit_card_number

    @credit_card_number.setter
    def credit_card_number(self, value):
        if not value or len(value) != 16:
            raise ValueError(f"Invalid credit card number: {value}")
        self._credit_card_number = value

    @property
    def expiration_date(self):  # pylint: disable=missing-function-docstring
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, value):
        if not value:
            raise ValueError(f"Invalid expiration date: {value}")

        # Auto parse the datetime input
        try:
            self._expiration_date = dtparse(value)
        except TypeError:
            raise ValueError(f"Invalid expiration date: {value}")

        # Check if the parsed datetime is less than right now
        if self._expiration_date < datetime.now():
            raise ValueError(f"Card already expired on {self._expiration_date}")

    @property
    def security_code(self):  # pylint: disable=missing-function-docstring
        return self._security_code

    @security_code.setter
    def security_code(self, value):
        if not value or len(value) != 3 or not value.isdigit():
            raise ValueError(f"Invalid security code: {value}")
        self._security_code = value
