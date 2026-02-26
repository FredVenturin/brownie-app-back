from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.error_handler import error_handler


class UpdateOrderStatus:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository


    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:

            order_id = http_request.path_params["order_id"]
            status = http_request.body["status"]

            updated = self.__orders_repository.edit_registry(
                order_id,
                {"status": status}
            )

            if not updated:
                raise HttpNotFoundError("Order not found")

            return HttpResponse(
                body={
                    "data": {
                        "type": "Order",
                        "id": order_id,
                        "status": status
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)