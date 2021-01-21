"""Module containing routes for payment processing."""

from flask import Blueprint
from flask import request

from app.model import Payment
from app.gateways import GatewayController


# API Blueprint
payment_bp = Blueprint('api', __name__)


@payment_bp.route('/ProcessPayment', methods=['POST'])
def process_payment():
    """Processes the input payment."""
    try:
        # Parse and validate the request data
        payment = Payment.from_dict(request.get_json(force=True))

        # Run gateway logic and get the actual gateway class
        controller = GatewayController(payment)
        gateway = controller.get_gateway()  # pylint: disable=unused-variable

        return {"message": "OK", "status_code": 200}, 200

    except ValueError:
        return {"message": "bad request", "status_code": 400}, 400

    return {"message": "internal server error", "status_code": 500}, 500
