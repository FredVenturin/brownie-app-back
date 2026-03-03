from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.error_handler import error_handler
from src.utils.orders_filter_builder import build_orders_doc_filter


class DeleteManyOrders:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository


    def delete_many(self, http_request: HttpRequest) -> HttpResponse:

        try:

            body = http_request.body

            filter = body["filter"]

            deleted_count = self.__delete_orders(filter)

            return HttpResponse(
                body={
                    "data": {
                        "type": "Orders",
                        "deleted": deleted_count,
                        "message": "Orders deleted successfully"
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)


    def __delete_orders(self, filter: dict) -> int:
        doc_filter = build_orders_doc_filter(filter)

        deleted_count = self.__orders_repository.delete_many_registries(doc_filter)

        if deleted_count == 0:
            raise HttpNotFoundError("No orders were deleted")

        return deleted_count