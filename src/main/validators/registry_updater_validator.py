from cerberus import Validator
from  src.errors.types.http_unprocessable_entity import HttpUnprocessableEntityError


def registry_updater_validator(body: any):
    body_validator = Validator({
        "data": {
            "type": "dict",
            "schema": {
                "name": {"type": "string"},
                "address": {"type": "string"},
                "cupom": {"type": "boolean"},
            }  
        }
    })

    response = body_validator.validate(body)
    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)