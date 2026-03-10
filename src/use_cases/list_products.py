from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class ListProducts:
    def __init__(self, products_repository):
        self.__products_repository = products_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            qp = http_request.query_params or {}

            page = int(qp.get("page", 1))
            limit = int(qp.get("limit", 10))

            products = self.__products_repository.list_with_pagination(page, limit)
            total = self.__products_repository.count_documents()

            return HttpResponse(
                status_code=200,
                body={
                    "data": {
                        "attributes": products,
                        "meta": {
                            "page": page,
                            "limit": limit,
                            "total": total
                        }
                    }
                }
            )

        except Exception as exception:
            return error_handler(exception)