from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class ListOrdersPaginated:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository


    def execute(self, http_request: HttpRequest) -> HttpResponse:

        try:

            query_params = http_request.query_params or {}

            page = int(query_params.get("page", 1))
            limit = int(query_params.get("limit", 10))

            status = query_params.get("status")

            doc_filter = {}

            if status:
                doc_filter["status"] = status

            orders = self.__orders_repository.select_with_pagination(doc_filter, page, limit)

            for order in orders:
                order["_id"] = str(order["_id"])

            return HttpResponse(
                body={
                    "data": {
                        "page": page,
                        "limit": limit,
                        "count": len(orders),
                        "orders": orders
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)