"""Tests for the payment request model."""
# pylint: disable=missing-function-docstring

import json as jsonlib
import pytest

from app.model import Payment

from app.utils.test_utils import INVALID_INITIAL_TEST_DICT
from app.utils.test_utils import VALID_INITIAL_TEST_DICT


def test__payment_model__valid_dictionary_input():
    payment = Payment.from_dict(VALID_INITIAL_TEST_DICT)
    assert isinstance(payment, Payment)


def test__payment_model__invalid_dictionary_input():
    with pytest.raises(ValueError):
        Payment.from_dict(INVALID_INITIAL_TEST_DICT)


def test__payment_model__valid_json_input():
    payment = Payment.from_json(jsonlib.dumps(VALID_INITIAL_TEST_DICT))
    assert isinstance(payment, Payment)


def test__payment_model__invalid_json_input():
    with pytest.raises(ValueError):
        Payment.from_json(jsonlib.dumps(INVALID_INITIAL_TEST_DICT))


def test__payment_model__correct_or_same_values():
    from_dict = Payment.from_dict(VALID_INITIAL_TEST_DICT)
    from_json = Payment.from_json(jsonlib.dumps(VALID_INITIAL_TEST_DICT))

    assert from_dict.amount == from_json.amount
    assert from_dict.card_holder == from_json.card_holder
    assert from_dict.credit_card_number == from_json.credit_card_number
    assert from_dict.expiration_date == from_json.expiration_date
    assert from_dict.security_code == from_json.security_code


def test__payment_model__break_credit_card_number():
    payment = Payment.from_dict(VALID_INITIAL_TEST_DICT)
    with pytest.raises(ValueError):
        payment.credit_card_number = None


def test__payment_model__break_expiration_date_with_none():
    payment = Payment.from_dict(VALID_INITIAL_TEST_DICT)
    with pytest.raises(ValueError):
        payment.expiration_date = None


def test__payment_model__break_expiration_date_with_unparsable():
    payment = Payment.from_dict(VALID_INITIAL_TEST_DICT)
    with pytest.raises(ValueError):
        payment.expiration_date = 'FOO BAR dasdho9 *#(!'


def test__payment_model__break_expiration_date_with_expired_date():
    payment = Payment.from_dict(VALID_INITIAL_TEST_DICT)
    with pytest.raises(ValueError):
        payment.expiration_date = '19950101'


def test__payment_model__break_security_code():
    payment = Payment.from_dict(VALID_INITIAL_TEST_DICT)
    with pytest.raises(ValueError):
        payment.security_code = 'a8!'
