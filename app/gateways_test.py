"""Tests for the different payment provider gateways."""
# pylint: disable=missing-function-docstring

import json as jsonlib
import pytest

from app.gateways import CheapPaymentGateway
from app.gateways import ExpensivePaymentGateway
from app.gateways import FunctioningPaymentGateway
from app.gateways import GatewayController
from app.gateways import PaymentGateway
from app.gateways import PremiumPaymentGateway

from app.utils.test_utils import VALID_INITIAL_TEST_DICT


@pytest.mark.parametrize("input_amount, expected_class", [
    (1, CheapPaymentGateway),
    (19, CheapPaymentGateway),
    (21, ExpensivePaymentGateway),
    (499, ExpensivePaymentGateway),
    (500, ExpensivePaymentGateway),
    (501, PremiumPaymentGateway),
    (999, PremiumPaymentGateway),
    (99999, PremiumPaymentGateway)
])
def test__gateway_controller__valid_amounts(input_amount, expected_class):
    # We don't care about other fields in this test
    # so we can just put placeholder values
    input_data = VALID_INITIAL_TEST_DICT.copy()
    input_data.update({'Amount': input_amount})

    controller = GatewayController(input_data)
    PaymentGateway = controller.get_gateway()

    assert PaymentGateway == expected_class


@pytest.mark.parametrize("input_amount", [-9999, -1, 0, 20])
def test__gateway_controller__invalid_amounts(input_amount):
    with pytest.raises(ValueError):
        # We don't care about other fields in this test
        # so we can just put placeholder values
        input_data = VALID_INITIAL_TEST_DICT.copy()
        input_data.update({'Amount': input_amount})

        controller = GatewayController(input_data)
        controller.get_gateway()


def test__gateway__dictionary_input():
    gateway = PaymentGateway(VALID_INITIAL_TEST_DICT)
    assert isinstance(gateway, PaymentGateway)


def test__payment_gateway__json_input():
    gateway = PaymentGateway(jsonlib.dumps(VALID_INITIAL_TEST_DICT))
    assert isinstance(gateway, PaymentGateway)


def test__functioning_payment_gateway__process():
    gateway = FunctioningPaymentGateway(VALID_INITIAL_TEST_DICT)
    assert gateway.process() == True
