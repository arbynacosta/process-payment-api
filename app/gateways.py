"""Module for the different payment provider gateways."""

from dataclasses import dataclass

from app.model import Payment


@dataclass
class PaymentGateway():
    """Base class for any payment gateway."""
    def __init__(self, payment):
        self.payment = payment

        # Check if the input is a dictionary
        # convert to a Payment object if true
        if isinstance(self.payment, dict):
            self.payment = Payment.from_dict(self.payment)

        # Check if input is still a raw JSON string
        if isinstance(self.payment, str):
            self.payment = Payment.from_json(self.payment)


class FunctioningPaymentGateway(PaymentGateway):
    """Basically everything that is not a controller."""
    def process(self):  # pylint: disable=no-self-use
        """No actual processing right now, just return true."""
        return True


class CheapPaymentGateway(FunctioningPaymentGateway):
    """Gateway for payments less than £20."""


class ExpensivePaymentGateway(FunctioningPaymentGateway):
    """Gateway for payments from £21 to £500."""


class PremiumPaymentGateway(FunctioningPaymentGateway):
    """Gateway for payments greater than £500."""


class GatewayController(PaymentGateway):
    """Controller class that decides what gateway to actually use."""

    def get_gateway(self):
        """Returns the proper gateway class based on the input request.

        Returns:
            - if the amount is less than £20, it's cheap
            - if the amount is between £21 and £500, it's expensive
            - if the amount is greater than £500, it's premium
        """
        if 1 <= self.payment.amount < 20:
            return CheapPaymentGateway

        if 21 <= self.payment.amount <= 500:
            return ExpensivePaymentGateway

        if self.payment.amount > 500:
            return PremiumPaymentGateway

        raise ValueError(f"Invalid amount: {self.payment.amount}")
