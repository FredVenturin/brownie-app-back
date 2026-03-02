from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.errors.error_handler import error_handler
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from datetime import datetime
from src.main.validators.registry_order_validator import registry_order_validator
from datetime import datetime, time

class RegistryOrder:
    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def registry(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body
            self.__validate_body(body)

            new_order = self.__format_new_order(body)
            self.__registry_order(new_order)

            return self.__format_response()
        except Exception as exception:
            return error_handler(exception)
        

    def __validate_body(self, body: dict) ->None:
        registry_order_validator(body)

    def __parse_order_date(self, date_str: str) -> datetime:
        # Espera "YYYY-MM-DD"
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return datetime.combine(d, time.min)  # 00:00:00

    def __format_new_order(self, body: dict) -> dict:
        new_order = body["data"]

        created_at = datetime.now()
        order_date_str = new_order.get("order_date")

        if order_date_str:
            order_date = self.__parse_order_date(order_date_str)
        else:
            order_date = created_at

        new_order = {
            **new_order,
            "created_at": created_at,
            "order_date": order_date,
            "status": new_order.get("status", "created"),
        }

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

