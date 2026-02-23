import pytest
from .registry_order_validator import registry_order_validator


def test_registry_order_validator():
    body = {
        "data": {
            "name": "joaozinho",
            "address": "rua do limao",
            "cupom": False,
            "itens": [
                {"item": "Refrigerante", "quantidade": 2},
                {"item": "pizza", "quantidade": 3}
            ]
        }
    }

    registry_order_validator(body)


def test_registry_order_validator_with_errors():
    body_with_error = {
        "data": {
            "name": "joaozinho",
            "address": "rua do limao",
            "cupom": "False",
            "itens": [
                {"item": "Refrigerante", "quantidade": 2},
                {"item": "pizza", "quantidade": 3}
            ]
        }
    }

    with pytest.raises(Exception):
        registry_order_validator(body_with_error)