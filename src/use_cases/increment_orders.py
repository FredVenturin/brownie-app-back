from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.error_handler import error_handler
from src.utils.orders_filter_builder import build_orders_doc_filter


class IncrementOrders:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository


    def increment(self, http_request: HttpRequest) -> HttpResponse:

        try:

            body = http_request.body

            filter = body["filter"]
            increment = body["increment"]

            modified_count = self.__increment_orders(filter, increment)

            return HttpResponse(
                body={
                    "data": {
                        "type": "Orders",
                        "modified": modified_count,
                        "message": "Orders incremented successfully"
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)


    def __increment_orders(self, filter: dict, increment: dict) -> int:
        doc_filter = build_orders_doc_filter(filter)

        modified_count = self.__orders_repository.edit_registry_with_increment(
            doc_filter,
            increment
        )

        if modified_count == 0:
            raise HttpNotFoundError("No orders were incremented")

        return modified_count