from datetime import datetime, time
from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.main.validators.registry_updater_validator import registry_updater_validator
from src.errors.error_handler import error_handler


class RegistryUpdater:
    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def update(self, http_request: HttpRequest) -> HttpResponse:
        try:
            order_id = http_request.path_params["order_id"]
            body = http_request.body
            self.__validate_body(body)

            self.__update_order(order_id, body)
            return self.__format_response(order_id)
        except Exception as exception:
            return error_handler(exception)

    def __validate_body(self, body: dict) -> None:
        registry_updater_validator(body)

    def __update_order(self, order_id: str, body: dict) -> None:
        update_data = body["data"] or {}

        # Nunca permitir mexer no id
        update_data.pop("_id", None)
        update_data.pop("id", None)

        # Normaliza order_date: se vier "YYYY-MM-DD", salva como datetime
        order_date = update_data.get("order_date")
        if isinstance(order_date, str) and order_date.strip():
            d = datetime.strptime(order_date.strip(), "%Y-%m-%d").date()
            update_data["order_date"] = datetime.combine(d, time.min)

        # Se vier itens, recalcula o prices.total automaticamente
        itens = update_data.get("itens")
        if isinstance(itens, list):
            total = 0.0
            for it in itens:
                qtd = float(it.get("quantidade", 0) or 0)
                price = float(it.get("price", 0) or 0)
                total += qtd * price

            prices = update_data.get("prices") or {}
            prices["total"] = total
            update_data["prices"] = prices

        self.__orders_repository.edit_registry(order_id, update_data)

    def __format_response(self, order_id: str) -> HttpResponse:
        return HttpResponse(
            body={
                "data": {
                    "type": "Order",
                    "id": order_id,
                    "updated": True
                }
            },
            status_code=200
        )