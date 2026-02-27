from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.error_handler import error_handler


class FilterOrders:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository


    def filters(self, http_request: HttpRequest) -> HttpResponse:

        try:

            filters = http_request.query_params

            orders = self.__filter_orders(filters)

            return HttpResponse(
                body={
                    "data": {
                        "type": "Orders",
                        "count": len(orders),
                        "attributes": orders
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)


    def __filter_orders(self, filters: dict) -> list:

        cursor = self.__orders_repository.select_many(filters)

        orders = list(cursor)

        if not orders:
            raise HttpNotFoundError("Orders not found")

        for order in orders:
            order["_id"] = str(order["_id"])

        return orders