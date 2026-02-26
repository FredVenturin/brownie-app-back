from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class CountOrders:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository


    def execute(self, http_request: HttpRequest) -> HttpResponse:

        try:

            query_params = http_request.query_params or {}

            status = query_params.get("status")

            doc_filter = {}

            if status:
                doc_filter["status"] = status

            count = self.__orders_repository.count_documents(doc_filter)

            return HttpResponse(
                body={
                    "data": {
                        "count": count
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)