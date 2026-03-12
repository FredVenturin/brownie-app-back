from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler
from src.utils.order_serializer import serialize_order


class FilterDeletedOrders:

    def __init__(self, orders_repository):
        self.__orders_repository = orders_repository

    def filters(self, http_request: HttpRequest) -> HttpResponse:
        try:
            qp = http_request.query_params or {}

            page = int(qp.get("page", 1))
            limit = int(qp.get("limit", 10))

            doc_filter = {}

            orders = self.__orders_repository.select_deleted_with_pagination(doc_filter, page, limit)
            orders = [serialize_order(order) for order in orders]
            total = self.__orders_repository.count_deleted_documents({})

            return HttpResponse(
                body={
                    "data": {
                        "attributes": orders,
                        "meta": {
                            "page": page,
                            "limit": limit,
                            "total": total
                        }
                    }
                },
                status_code=200
            )

        except Exception as exception:
            return error_handler(exception)