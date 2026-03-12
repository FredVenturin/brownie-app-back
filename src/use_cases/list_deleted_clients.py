from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.errors.error_handler import error_handler


class ListDeletedClients:

    def __init__(self, clients_repository):
        self.__clients_repository = clients_repository

    def execute(self, http_request: HttpRequest) -> HttpResponse:
        try:
            qp = http_request.query_params or {}

            page = int(qp.get("page", 1))
            limit = int(qp.get("limit", 10))

            clients = self.__clients_repository.list_deleted_with_pagination(page, limit)
            total = self.__clients_repository.count_deleted_documents()

            return HttpResponse(
                body={
                    "data": {
                        "attributes": clients,
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