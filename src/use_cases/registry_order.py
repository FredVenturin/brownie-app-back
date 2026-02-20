from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from datetime import datetime

class RegistryOrder:
    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def registry(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            new_order = self.__format_new_order(body)
            self.__registry_order(new_order)

            return self.__format_response()
        except Exception as exception:
            return HttpResponse(
                body={"error": exception},
                status_code=400
            )

    def __format_new_order(self, body: dict) -> dict:
        new_order = body["data"]
        new_order = {**new_order, "created_at": datetime.now()}
        return new_order

    def __registry_order(self, new_order: dict) -> None:
        self.__orders_repository.insert_document(new_order)

    def __format_response(self) ->dict:
        return HttpResponse(
            body={
                "data": {
                    "type": "Order",
                    "count": 1,
                    "registry": True
                }
            },
            status_code=201
        )

