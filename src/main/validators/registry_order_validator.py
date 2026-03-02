from cerberus import Validator
from src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


def registry_order_validator(body: any):

    body_validator = Validator({

        "data": {
            "type": "dict",
            "required": True,

            "schema": {

                # obrigatório
                "name": {
                    "type": "string",
                    "required": True,
                    "empty": False
                },

                # obrigatório
                "itens": {
                    "type": "list",
                    "required": True,
                    "minlength": 1,

                    "schema": {
                        "type": "dict",

                        "schema": {

                            "item": {
                                "type": "string",
                                "required": True
                            },

                            "quantidade": {
                                "type": "integer",
                                "required": True,
                                "min": 1
                            },

                            # novo campo preço por item
                            "price": {
                                "type": "float",
                                "required": True,
                                "min": 0
                            },
                            "cost": {
                                "type": "float",
                                "required": True,
                                "min": 0
                            }
                        }
                    }
                },

                # opcional
                "address": {
                    "type": "string",
                    "required": False
                },

                # opcional
                "cupom": {
                    "type": "boolean",
                    "required": False
                },

                # Obrigatorio com valores permitidos
                "status": {
                    "type": "string",
                    "required": True,
                    "allowed": [
                        "confirmed",
                        "preparing",
                        "sold",
                        "cancelled"
                    ]
                },

                # novo objeto prices
                "prices": {
                    "type": "dict",
                    "required": True,

                    "schema": {

                        "total": {
                            "type": "float",
                            "required": True,
                            "min": 0
                        },

                        "delivery": {
                            "type": "float",
                            "required": False,
                            "min": 0
                        },

                        "discount": {
                            "type": "float",
                            "required": False,
                            "min": 0
                        }
                    }
                },

                # opcional
                "sold_at": {
                    "type": "string",
                    "required": False
                }
            }
        }
    })

    response = body_validator.validate(body)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)