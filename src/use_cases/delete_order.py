from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.types.http_not_found import HttpNotFoundError
from src.errors.error_handler import error_handler


class RegistryDeleter:
    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def delete(self, http_request: HttpRequest) -> HttpResponse:
        try:
            order_id = http_request.path_params["order_id"]

            deleted = self.__delete_order(order_id)

            return HttpResponse(
                body={
                    "data": {
                        "type": "Order",
                        "id": order_id,
                        "message": "Order deleted successfully"
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)

    def __delete_order(self, order_id: str) -> bool:

        deleted = self.__orders_repository.delete_registry(order_id)

        if not deleted:
            raise HttpNotFoundError("Order not found")

        return True