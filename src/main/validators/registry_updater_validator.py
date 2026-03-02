from cerberus import Validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError

def registry_updater_validator(body: any):

    body_validator = Validator({
        "data": {
            "type": "dict",
            "required": True,
            "schema": {

                "name": {"type": "string", "required": False},
                "address": {"type": "string", "required": False},
                "cupom": {"type": "boolean", "required": False},

                "status": {
                    "type": "string",
                    "required": False,
                    "allowed": ["confirmed", "preparing", "sold", "cancelled"]
                },

                "prices": {
                    "type": "dict",
                    "required": False,
                    "schema": {
                        "total": {"type": "float", "required": False, "min": 0},
                        "delivery": {"type": "float", "required": False, "min": 0},
                        "discount": {"type": "float", "required": False, "min": 0},
                    }
                },

                "sold_at": {"type": "string", "required": False},

                "itens": {
                    "type": "list",
                    "required": False,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "item": {"type": "string", "required": False},
                            "quantidade": {"type": "integer", "required": False, "min": 1},
                            "price": {"type": "float", "required": False, "min": 0},
                            "cost": {"type": "float", "required": False, "min": 0},
                        }
                    }
                },
            }
        }
    })

    if not body_validator.validate(body):
        raise HttpUnprocessableEntityError(body_validator.errors)