from cerberus import Validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


def registry_updater_validator(body: any):

    body_validator = Validator({

        "data": {
            "type": "dict",
            "required": True,
            "empty": False,

            "schema": {

                "name": {
                    "type": "string",
                    "required": False,
                    "empty": False
                },

                "address": {
                    "type": "string",
                    "required": False
                },

                "cupom": {
                    "type": "boolean",
                    "required": False
                },

                "status": {
                    "type": "string",
                    "required": False,
                    "allowed": [
                        "confirmed",
                        "preparing",
                        "sold",
                        "cancelled"
                    ]
                },

                "itens": {
                    "type": "list",
                    "required": False,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "item": {"type": "string"},
                            "quantidade": {"type": "integer", "min": 1},
                            "price": {"type": "float", "min": 0}
                        }
                    }
                },

                "prices": {
                    "type": "dict",
                    "required": False,
                    "schema": {
                        "total": {"type": "float", "min": 0},
                        "delivery": {"type": "float", "min": 0},
                        "discount": {"type": "float", "min": 0}
                    }
                },

                "sold_at": {
                    "type": "string",
                    "required": False
                }
            },

            "allow_unknown": True
        }
    })

    response = body_validator.validate(body)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)