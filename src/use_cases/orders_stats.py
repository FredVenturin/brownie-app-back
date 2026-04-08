from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class OrdersStats:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            stats = self.__orders_repository.count_by_status()

            return HttpResponse(
                body={"data": {"attributes": stats}},
                status_code=200,
            )

        except Exception as exception:
            return error_handler(exception)
