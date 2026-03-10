from src.models.repository.interfaces.orders_repository_interface import OrdersRepositoryInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler
from src.utils.order_serializer import serialize_order



class ListOrdersPaginated:

    def __init__(self, orders_repository: OrdersRepositoryInterface):
        self.__orders_repository = orders_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            query_params = http_request.query_params or {}

            page = int(query_params.get("page", 1))
            limit = int(query_params.get("limit", 10))

            doc_filter = {}

            orders = self.__orders_repository.select_with_pagination(
                doc_filter, page, limit
            )

            orders = [serialize_order(o) for o in orders]

            return HttpResponse(
                body={
                    "data": {
                        "type": "Orders",
                        "attributes": orders
                    },
                    "meta": {
                        "page": page,
                        "limit": limit,
                        "total": len(orders),
                        "has_next": len(orders) == limit
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)